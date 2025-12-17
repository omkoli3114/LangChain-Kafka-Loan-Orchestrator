from utils.pdf_generator import create_sanction_letter

def generate_sanction(customer_name: str, amount: float, tenure_months: int, interest_rate: float):
    """
    Calculates EMI and generates the sanction letter.
    """
    # Calculate EMI
    r = interest_rate / 12 / 100
    n = tenure_months
    if r > 0:
        emi = amount * r * ((1 + r)**n) / (((1 + r)**n) - 1)
    else:
        emi = amount / n

    # Generate PDF
    pdf_base64 = create_sanction_letter(
        customer_name=customer_name,
        amount=amount,
        tenure=tenure_months,
        interest_rate=interest_rate,
        emi=emi
    )
    
    return {
        "success": True,
        "pdf_base64": pdf_base64,
        "emi": round(emi, 2)
    }
