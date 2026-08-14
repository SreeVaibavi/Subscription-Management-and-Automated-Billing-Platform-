from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

from app.database.connection import get_db
import app.models.core as models

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)

# --- SCHEMAS FOR INCOMING WEBHOOK PAYLOAD ---
class WebhookData(BaseModel):
    invoice_id: str
    customer_id: str
    amount_attempted: float
    currency: str
    status: str
    failure_reason: str | None = None

class PaymentWebhookPayload(BaseModel):
    event_id: str
    type: str
    data: WebhookData

# --- THE WEBHOOK LISTENER ENDPOINT ---
@router.post("/payments")
async def payment_event_webhook(payload: PaymentWebhookPayload, db: Session = Depends(get_db)):
    """
    Receives payment events from the mock gateway (or Stripe).
    Updates invoice statuses and subscription access based on payment success/failure.
    """
    logger.info(f"Received webhook event: {payload.type}")
    
    event_type = payload.type
    data = payload.data
    
    # 1. Validate the Invoice exists in our database
    invoice = db.query(models.Invoice).filter(models.Invoice.id == data.invoice_id).first()
    if not invoice:
        logger.error(f"Webhook Error: Invoice {data.invoice_id} not found.")
        raise HTTPException(status_code=404, detail="Invoice not found")

    # 2. Record the actual Payment Attempt in the database
    # For refunds, we treat the 'refunded' status as a successful transaction of the negative amount
    payment_status = models.PaymentStatus.succeeded if data.status in ["succeeded", "refunded"] else models.PaymentStatus.failed
    
    new_payment = models.Payment(
        invoice_id=invoice.id,
        customer_id=data.customer_id,
        amount=data.amount_attempted,
        currency=data.currency,
        status=payment_status,
        payment_method="mock_card_processor"
    )
    db.add(new_payment)
    
    # 3. Handle the Business Logic based on the Event Type
    if event_type == "payment_intent.succeeded":
        # Mark invoice as successfully paid
        invoice.status = models.InvoiceStatus.paid
        invoice.amount_paid = data.amount_attempted
        
        db.commit()
        logger.info(f"SUCCESS: Invoice {invoice.invoice_number} marked as PAID.")
        
    elif event_type == "payment_intent.failed":
        # Mark invoice as uncollectible
        invoice.status = models.InvoiceStatus.uncollectible
        
        # Security: Find the linked subscription and FREEZE their account!
        if invoice.subscription_id:
            sub = db.query(models.Subscription).filter(models.Subscription.id == invoice.subscription_id).first()
            if sub and sub.status == models.SubscriptionState.active:
                old_status = sub.status
                sub.status = models.SubscriptionState.past_due
                
                # Audit Log the automatic downgrade
                audit = models.AuditLog(
                    entity_type="Subscription",
                    entity_id=sub.id,
                    action="AUTO_DOWNGRADED_TO_PAST_DUE",
                    old_value=old_status.value,
                    new_value=sub.status.value
                )
                db.add(audit)
                logger.warning(f"FAILURE: Subscription {sub.id} locked to PAST_DUE due to payment failure.")
                
        db.commit()
        
    elif event_type == "payment_intent.refunded":
        # Mark the negative refund invoice as officially processed (paid out to the user)
        invoice.status = models.InvoiceStatus.paid
        invoice.amount_paid = data.amount_attempted 
        
        db.commit()
        logger.info(f"REFUND SUCCESS: Invoice {invoice.invoice_number} marked as PAID OUT to customer.")
        
    return {"status": "success", "message": "Webhook processed safely"}