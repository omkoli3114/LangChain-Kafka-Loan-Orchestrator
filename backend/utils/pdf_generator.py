import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def create_sanction_letter(customer_name: str, amount: float, tenure: int, interest_rate: float, emi: float):
    """
    Generates a sanction letter PDF and returns the base64 encoded string.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "NBFC Personal Loan Sanction Letter")
    
    # Date
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Customer Details
    c.drawString(50, height - 120, f"Dear {customer_name},")
    c.drawString(50, height - 140, "We are pleased to inform you that your personal loan has been sanctioned.")
    
    # Loan Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 180, "Loan Details:")
    c.setFont("Helvetica", 12)
    
    details = [
        f"Sanctioned Amount: INR {amount:,.2f}",
        f"Tenure: {tenure} months",
        f"Interest Rate: {interest_rate}% p.a.",
        f"Monthly EMI: INR {emi:,.2f}"
    ]
    
    y = height - 210
    for detail in details:
        c.drawString(80, y, detail)
        y -= 20
        
    # Footer
    c.drawString(50, y - 40, "Terms and conditions apply.")
    c.drawString(50, y - 60, "This is a computer-generated document and does not require a signature.")
    
    c.save()
    
    buffer.seek(0)
    pdf_bytes = buffer.read()
    return base64.b64encode(pdf_bytes).decode('utf-8')
