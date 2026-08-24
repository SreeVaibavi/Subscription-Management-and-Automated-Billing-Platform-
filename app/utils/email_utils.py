import io
import html
import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

from app.core.pdf_generator import generate_invoice_pdf
from app.database.connection import SessionLocal
from app.models.core import Customer, Invoice

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = (os.getenv("SMTP_EMAIL") or "").strip()
SMTP_PASSWORD = "".join((os.getenv("SMTP_PASSWORD") or "").split())


def _send_message(message: MIMEMultipart) -> None:
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        logger.warning("SMTP_EMAIL or SMTP_PASSWORD is not configured; email skipped.")
        return

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(message)
    except smtplib.SMTPAuthenticationError:
        logger.exception(
            "Gmail rejected SMTP credentials. Use a Gmail App Password for %s.",
            SMTP_EMAIL,
        )
    except (OSError, smtplib.SMTPException):
        logger.exception("SMTP delivery failed for %s.", message.get("To"))


def _email_shell(title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html><body style="margin:0;background:#f3f4f6;font-family:Inter,Helvetica,Arial,sans-serif;color:#1f2937;">
  <div style="padding:40px 16px;">
    <div style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;overflow:hidden;">
      <div style="background:#E8453C;padding:24px 32px;color:#ffffff;">
        <div style="font-size:22px;font-weight:800;">BillWise</div>
        <div style="font-size:12px;letter-spacing:1.5px;text-transform:uppercase;opacity:.85;margin-top:4px;">Automated billing</div>
      </div>
      <div style="padding:32px;">
        <h1 style="margin:0 0 16px;font-size:24px;color:#111827;">{title}</h1>
        {body_html}
      </div>
      <div style="padding:20px 32px;background:#f9fafb;color:#6b7280;font-size:12px;">This is an automated message from BillWise.</div>
    </div>
  </div>
</body></html>"""


def send_welcome_email(user_email: str, user_name: str) -> None:
    safe_name = html.escape(user_name)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to BillWise"
    message["From"] = SMTP_EMAIL or ""
    message["To"] = user_email
    body = f"""
        <p style="font-size:16px;line-height:1.6;">Hi {safe_name},</p>
        <p style="font-size:16px;line-height:1.6;">Welcome to BillWise. Your account is ready for automated billing and subscription management.</p>
        <p style="margin:28px 0;"><a href="#" style="display:inline-block;background:#E8453C;color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;">Open BillWise</a></p>
    """
    message.attach(MIMEText(_email_shell("Welcome to BillWise", body), "html", "utf-8"))
    _send_message(message)


def send_payment_receipt(
    user_email: str,
    invoice_number: str,
    amount: float,
    pdf_bytes: bytes,
) -> None:
    safe_invoice_number = html.escape(invoice_number)
    message = MIMEMultipart("mixed")
    message["Subject"] = f"Payment receipt for {safe_invoice_number}"
    message["From"] = SMTP_EMAIL or ""
    message["To"] = user_email
    body = f"""
        <p style="font-size:16px;line-height:1.6;">Your payment was received successfully.</p>
        <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:16px;margin:24px 0;">
          <div style="color:#6b7280;font-size:12px;text-transform:uppercase;">Invoice</div>
          <div style="font-size:18px;font-weight:800;margin-top:4px;">{safe_invoice_number}</div>
          <div style="color:#6b7280;font-size:12px;text-transform:uppercase;margin-top:14px;">Amount paid</div>
          <div style="font-size:22px;font-weight:800;color:#E8453C;margin-top:4px;">${amount:,.2f}</div>
        </div>
        <p style="font-size:14px;line-height:1.6;color:#6b7280;">Your invoice is attached as a PDF for your records.</p>
    """
    message.attach(MIMEText(_email_shell("Payment received", body), "html", "utf-8"))

    attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=f"{safe_invoice_number}.pdf",
    )
    message.attach(attachment)
    _send_message(message)


def send_payment_receipt_for_invoice(invoice_id: str) -> None:
    """Load billing data with a task-local session before sending a receipt."""
    db = SessionLocal()
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            logger.error("Cannot send receipt: invoice %s was not found.", invoice_id)
            return

        customer = db.query(Customer).filter(Customer.id == invoice.customer_id).first()
        if not customer:
            logger.error("Cannot send receipt: customer for invoice %s was not found.", invoice_id)
            return

        pdf_buffer: io.BytesIO = generate_invoice_pdf(invoice, customer)
        send_payment_receipt(
            customer.email,
            invoice.invoice_number,
            invoice.amount_paid or invoice.amount_due,
            pdf_buffer.getvalue(),
        )
    except Exception:
        logger.exception("Failed to send payment receipt for invoice %s.", invoice_id)
    finally:
        db.close()