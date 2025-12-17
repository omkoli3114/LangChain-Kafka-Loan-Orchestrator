from mock_servers.crm import get_customer_by_phone

def verify_kyc(phone: str, stated_address: str):
    """
    Verifies customer details against mock CRM.
    """
    customer = get_customer_by_phone(phone)
    if not customer:
        return {"verified": False, "reason": "Customer not found in records"}
    
    # Simple simplistic string matching
    address_match = stated_address.lower() in customer["address"].lower() or customer["address"].lower() in stated_address.lower()
    
    return {
        "verified": True,
        "phone_match": True,
        "address_match": address_match,
        "customer_id": customer["id"],
        "customer_name": customer["name"]
    }
