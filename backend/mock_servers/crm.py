import json
from pathlib import Path
from typing import Optional

# Load customer data
DATA_FILE = Path(__file__).parent.parent / "data" / "customers.json"

def get_customers():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def get_customer_by_phone(phone: str) -> Optional[dict]:
    customers = get_customers()
    for cust in customers:
        if cust["phone"] == phone:
            return cust
    return None

def get_customer_by_id(customer_id: str) -> Optional[dict]:
    customers = get_customers()
    for cust in customers:
        if cust["id"] == customer_id:
            return cust
    return None
