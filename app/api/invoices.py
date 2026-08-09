from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import database connection and models
from app.database.connection import get_db
import app.models.core as models
from app.api.subscriptions import get_current_customer

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

# 1. GET ALL INVOICES (Admin View)
@router.get("/")
def get_all_invoices(db: Session = Depends(get_db)):
    """Fetches all invoices in the system for admin overview."""
    invoices = db.query(models.Invoice).all()
    return invoices

# 2. GET MY INVOICES (Customer View)
@router.get("/me")
def get_my_invoices(
    db: Session = Depends(get_db),
    customer: models.Customer = Depends(get_current_customer)
):
    """Fetches invoices belonging to the currently logged in customer."""
    invoices = db.query(models.Invoice).filter(models.Invoice.customer_id == customer.id).all()
    return invoices