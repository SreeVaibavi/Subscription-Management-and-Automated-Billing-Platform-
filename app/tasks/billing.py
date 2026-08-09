from datetime import datetime, timezone, timedelta
from app.core.celery_app import celery_app

# Import your database session and models
from app.database.connection import SessionLocal 
import app.models.core as models

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

            # 3. Generate the new Invoice
            new_invoice = models.Invoice(
                customer_id=sub.customer_id,
                subscription_id=sub.id,
                amount_due=plan.price,
                currency=plan.currency,
                status=models.InvoiceStatus.open,
                due_date=now + timedelta(days=7) # Give them 7 days to pay
            )
            db.add(new_invoice)
            
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