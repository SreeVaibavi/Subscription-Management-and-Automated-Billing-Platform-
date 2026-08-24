from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import jwt, JWTError
import uuid

# We need passlib to securely hash the new password if they change it
from passlib.context import CryptContext

from app.database.connection import get_db
import app.models.core as models
from app.core.notifications import notify_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# --- SECURITY & DEPENDENCIES ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
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
class UserProfileResponse(BaseModel):
    email: str
    full_name: str | None = None
    phone_number: str | None = None

class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    password: str | None = None


# --- ROUTES ---

# 1. GET PROFILE DATA
@router.get("/me/profile", response_model=UserProfileResponse)
def get_my_profile(customer: models.Customer = Depends(get_current_customer)):
    """Fetches the logged-in user's profile data to auto-fill the frontend form."""
    return {
        "email": customer.email,
        "full_name": customer.full_name,
        "phone_number": customer.phone_number
    }

# 2. UPDATE PROFILE DATA
@router.put("/me/profile")
def update_my_profile(
    profile_data: UserProfileUpdate, 
    db: Session = Depends(get_db), 
    customer: models.Customer = Depends(get_current_customer)
):
    """Updates the logged-in user's profile name, phone, and optionally their password."""
    
    if profile_data.full_name is not None:
        customer.full_name = profile_data.full_name
        
    if profile_data.phone_number is not None:
        customer.phone_number = profile_data.phone_number
        
    # If the user typed a new password into the form, securely hash it before saving
    if profile_data.password: 
        hashed_pw = pwd_context.hash(profile_data.password)
        customer.hashed_password = hashed_pw
        
    db.commit()

    # --- NEW: TRIGGER ADMIN NOTIFICATION ---
    notify_admin(db, f"Customer '{customer.email}' updated their profile details.")
    db.commit()

    return {"status": "success", "message": "Profile updated successfully!"}


# 3. GET ALL USERS (Admin View)
@router.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    """Fetches all registered users for the Admin Dashboard."""
    users = db.query(models.Customer).order_by(models.Customer.created_at.desc()).all()
    return users


# ==========================================
# --- NEW NOTIFICATION ENDPOINTS ---
# ==========================================

# 4. GET MY NOTIFICATIONS (Customer View)
@router.get("/me/notifications")
def get_my_notifications(db: Session = Depends(get_db), customer: models.Customer = Depends(get_current_customer)):
    """Fetches unread notifications specifically for the logged-in user."""
    notifs = db.query(models.Notification).filter(
        models.Notification.customer_id == customer.id,
        models.Notification.is_read == False
    ).order_by(models.Notification.created_at.desc()).all()
    return notifs

# 5. GET ADMIN NOTIFICATIONS (Admin View)
@router.get("/admin/notifications")
def get_admin_notifications(db: Session = Depends(get_db)):
    """Fetches global unread system alerts for the Administrator."""
    notifs = db.query(models.Notification).filter(
        models.Notification.customer_id == None,
        models.Notification.is_read == False
    ).order_by(models.Notification.created_at.desc()).all()
    return notifs

# 6. MARK NOTIFICATION AS READ
@router.put("/notifications/{notif_id}/read")
def mark_notification_read(notif_id: str, db: Session = Depends(get_db)):
    """Dismisses a notification by marking it as read."""
    notif = db.query(models.Notification).filter(models.Notification.id == notif_id).first()
    if notif:
        notif.is_read = True
        db.commit()
    return {"status": "success"}