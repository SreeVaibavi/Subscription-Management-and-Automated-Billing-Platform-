from datetime import datetime, timezone, timedelta
from app.core.celery_app import celery_app

# Import your database session and models
from app.database.connection import SessionLocal 
import app.models.core as models

# --- NEW: Import the math engine ---
from app.core import billing_math

@celery_app.task(name="app.tasks.billing.process_renewals")
def process_renewals():
    """
    Background job that finds active subscriptions due for renewal,
    generates a new invoice, and extends the subscription period.
    """
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    invoices_created = 0
    
    try:
        # 1. Find all active subscriptions where the billing period ends today (or passed)
        due_subscriptions = db.query(models.Subscription).filter(
            models.Subscription.status == models.SubscriptionState.active,
            models.Subscription.current_period_end <= now
        ).all()

        for sub in due_subscriptions:
            # Check if user requested cancellation at the end of this cycle
            if sub.cancel_at_period_end:
                sub.status = models.SubscriptionState.cancelled
                sub.canceled_at = now
                
                # Log cancellation
                db.add(models.AuditLog(
                    entity_type="Subscription",
                    entity_id=sub.id,
                    action="AUTO_CANCELLED_AT_PERIOD_END"
                ))
                db.commit()
                continue
                
            # 2. Get the plan to know how much to charge
            plan = db.query(models.Plan).filter(models.Plan.id == sub.plan_id).first()
            if not plan:
                continue

            # 3. Generate the new Invoice using the math engine
            invoice = billing_math.generate_standard_invoice(db, sub, plan)
            
            # Set the due date for 7 days from now
            invoice.due_date = now + timedelta(days=7)
            
            # 4. Push the subscription dates forward for the next cycle
            sub.current_period_start = now
            if plan.billing_interval == "annual":
                sub.current_period_end = now + timedelta(days=365)
            else:
                sub.current_period_end = now + timedelta(days=30)
                
            db.commit()
            invoices_created += 1

        print(f"Billing Cycle Complete: {invoices_created} new invoices generated.")
        return f"Processed {invoices_created} renewals."

    except Exception as e:
        db.rollback()
        print(f"Error during billing cycle: {e}")
    finally:
        db.close()