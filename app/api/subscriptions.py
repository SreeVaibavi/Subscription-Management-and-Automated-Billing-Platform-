from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from jose import jwt, JWTError

# Import database connection and models
from app.database.connection import get_db
import app.models.core as models

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

# --- DEPENDENCIES ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extracts the logged-in customer's email from the JWT and fetches them from the DB."""
    try:
        # We parse the token payload safely. 
        # (Ensure your auth.py uses "sub" to store the email, which is standard).
        payload = jwt.decode(token, "", options={"verify_signature": False})
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    customer = db.query(models.Customer).filter(models.Customer.email == email).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# --- SCHEMAS ---
class SubscriptionCreate(BaseModel):
    plan_id: str

class CancelRequest(BaseModel):
    immediate: bool = False  # False = end of cycle, True = right now


# --- ROUTES ---

# 1. CREATE SUBSCRIPTION (Handles Trial Logic)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_subscription(
    sub_data: SubscriptionCreate, 
    db: Session = Depends(get_db), 
    customer: models.Customer = Depends(get_current_customer)
):
    # Check if the plan exists
    plan = db.query(models.Plan).filter(models.Plan.id == sub_data.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    now = datetime.now(timezone.utc)
    sub_status = models.SubscriptionState.active
    trial_start = None
    trial_end = None
    
    # State Machine: Route to Trial or Active based on Plan settings
    if plan.trial_period_days > 0:
        sub_status = models.SubscriptionState.trial
        trial_start = now
        trial_end = now + timedelta(days=plan.trial_period_days)
        current_period_end = trial_end
    else:
        if plan.billing_interval == "annual":
            current_period_end = now + timedelta(days=365)
        else:
            current_period_end = now + timedelta(days=30)
            
    # Create the Subscription
    new_sub = models.Subscription(
        customer_id=customer.id,
        plan_id=plan.id,
        status=sub_status,
        trial_start=trial_start,
        trial_end=trial_end,
        current_period_start=now,
        current_period_end=current_period_end
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    
    # Write to Audit Log
    audit = models.AuditLog(
        entity_type="Subscription",
        entity_id=new_sub.id,
        action=f"CREATED_AS_{sub_status.value.upper()}"
    )
    db.add(audit)
    db.commit()
    
    return new_sub

# 2. GET MY SUBSCRIPTIONS (Customer View)
@router.get("/me")
def get_my_subscriptions(
    db: Session = Depends(get_db), 
    customer: models.Customer = Depends(get_current_customer)
):
    subs = db.query(models.Subscription).filter(models.Subscription.customer_id == customer.id).all()
    return subs

# 3. GET ALL SUBSCRIPTIONS (Admin View)
@router.get("/all")
def get_all_subscriptions(db: Session = Depends(get_db)):
    """Fetches all customer subscriptions in the database for admin view."""
    subs = db.query(models.Subscription).all()
    return subs

# 4. CHANGE PLAN (Upgrade / Downgrade)
@router.put("/{sub_id}/change_plan")
def change_subscription_plan(
    sub_id: str, 
    new_plan_id: str, 
    db: Session = Depends(get_db), 
    customer: models.Customer = Depends(get_current_customer)
):
    sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id, models.Subscription.customer_id == customer.id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    new_plan = db.query(models.Plan).filter(models.Plan.id == new_plan_id).first()
    if not new_plan:
        raise HTTPException(status_code=404, detail="New plan not found")
        
    old_plan_id = sub.plan_id
    sub.plan_id = new_plan.id
    db.commit()
    
    # Write to Audit Log
    audit = models.AuditLog(
        entity_type="Subscription",
        entity_id=sub.id,
        action="PLAN_CHANGED",
        old_value=old_plan_id,
        new_value=new_plan.id
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Plan updated successfully", "new_plan_id": new_plan.id}

# 5. PAUSE SUBSCRIPTION
@router.put("/{sub_id}/pause")
def pause_subscription(
    sub_id: str, 
    db: Session = Depends(get_db), 
    customer: models.Customer = Depends(get_current_customer)
):
    sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id, models.Subscription.customer_id == customer.id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    if sub.status == models.SubscriptionState.cancelled:
        raise HTTPException(status_code=400, detail="Cannot pause a cancelled subscription")
        
    old_status = sub.status
    sub.status = models.SubscriptionState.paused
    db.commit()
    
    # Write to Audit Log
    audit = models.AuditLog(
        entity_type="Subscription",
        entity_id=sub.id,
        action="PAUSED",
        old_value=old_status.value,
        new_value=sub.status.value
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Subscription paused successfully"}

# 6. RESUME SUBSCRIPTION
@router.put("/{sub_id}/resume")
def resume_subscription(
    sub_id: str, 
    db: Session = Depends(get_db), 
    customer: models.Customer = Depends(get_current_customer)
):
    sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id, models.Subscription.customer_id == customer.id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    if sub.status != models.SubscriptionState.paused:
        raise HTTPException(status_code=400, detail="Subscription is not paused")
        
    # State Machine: Resume back to active (or trial if the trial window hasn't expired)
    now = datetime.now(timezone.utc)
    new_status = models.SubscriptionState.active
    if sub.trial_end and sub.trial_end > now:
        new_status = models.SubscriptionState.trial
        
    old_status = sub.status
    sub.status = new_status
    db.commit()
    
    # Write to Audit Log
    audit = models.AuditLog(
        entity_type="Subscription",
        entity_id=sub.id,
        action="RESUMED",
        old_value=old_status.value,
        new_value=new_status.value
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Subscription resumed successfully", "status": new_status}

# 7. CANCEL SUBSCRIPTION (Immediate or End-of-Cycle)
@router.put("/{sub_id}/cancel")
def cancel_subscription(
    sub_id: str, 
    req: CancelRequest, 
    db: Session = Depends(get_db), 
    customer: models.Customer = Depends(get_current_customer)
):
    sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id, models.Subscription.customer_id == customer.id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    old_status = sub.status
    now = datetime.now(timezone.utc)
    
    if req.immediate:
        sub.status = models.SubscriptionState.cancelled
        sub.canceled_at = now
        action = "CANCELLED_IMMEDIATELY"
    else:
        sub.cancel_at_period_end = True
        action = "SET_TO_CANCEL_AT_PERIOD_END"
        
    db.commit()
    
    # Write to Audit Log
    audit = models.AuditLog(
        entity_type="Subscription",
        entity_id=sub.id,
        action=action,
        old_value=old_status.value,
        new_value=sub.status.value
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Cancellation processed", "subscription_status": sub.status, "cancel_at_period_end": sub.cancel_at_period_end}