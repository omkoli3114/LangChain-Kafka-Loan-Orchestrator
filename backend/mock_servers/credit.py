from .crm import get_customer_by_id

def get_credit_score(customer_id: str):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}
    
    return {
        "customer_id": customer_id,
        "credit_score": customer["credit_score"],
        "report_date": "2024-01-01"
    }
