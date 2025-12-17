def evaluate_loan(credit_score: int, requested_amount: float, pre_approved_limit: float, monthly_salary: float = 0.0):
    """
    Evaluates loan application based on credit score, limits, and salary.
    """
    if credit_score < 700:
        return {
            "decision": "REJECT",
            "reason": "Credit score below 700"
        }
    
    if requested_amount <= pre_approved_limit:
        return {
            "decision": "APPROVE",
            "reason": "Within pre-approved limit"
        }
        
    if requested_amount <= 2 * pre_approved_limit:
        if monthly_salary > 0:
            # Check EMI logic (approximate EMI for 5 years at 14%)
            # P * r * (1+r)^n / ((1+r)^n - 1)
            # 5 years = 60 months
            annual_rate = 14.0
            r = annual_rate / 12 / 100
            n = 60
            emi = requested_amount * r * ((1 + r)**n) / (((1 + r)**n) - 1)
            
            if emi <= 0.5 * monthly_salary:
                return {
                    "decision": "APPROVE",
                    "reason": "Salary supports EMI",
                    "emi": round(emi, 2)
                }
            else:
                return {
                    "decision": "REJECT",
                    "reason": "EMI exceeds 50% of monthly salary",
                    "emi": round(emi, 2)
                }
        else:
            return {
                "decision": "REQUEST_SALARY_SLIP",
                "reason": "Amount > limit but <= 2x limit. Need salary slip."
            }
            
    return {
        "decision": "REJECT",
        "reason": "Amount exceeds 2x pre-approved limit"
    }
