from sqlalchemy.orm import Session

from app.models.core import Customer, Notification


def notify_admin(db: Session, message: str) -> None:
    db.add(Notification(customer_id=None, message=message))


def notify_customers(db: Session, message: str) -> None:
    customer_ids = [customer_id for (customer_id,) in db.query(Customer.id).filter(
        Customer.is_admin == False
    ).all()]
    db.add_all([
        Notification(customer_id=customer_id, message=message)
        for customer_id in customer_ids
    ])
