def negotiate_loan(requested_amount: float, pre_approved_limit: float):
    """
    Negotiates loan terms based on rules.
    """
    if requested_amount <= pre_approved_limit:
        return {
            "interest_rate": 12.0,
            "status": "APPROVED_BASE_RATE",
            "message": "We can offer you this loan at our best rate of 12% per annum."
        }
    else:
        return {
            "interest_rate": 14.0,
            "status": "APPROVED_HIGHER_RATE",
            "message": "Since this amount exceeds your pre-approved limit, we can offer it at a rate of 14% per annum."
        }
