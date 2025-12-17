from .crm import get_customer_by_id

def get_offer(customer_id: str):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}
    
    return {
        "customer_id": customer_id,
        "pre_approved_limit": customer["pre_approved_limit"],
        "product": "Personal Loan",
        "valid_until": "2025-12-31"
    }
