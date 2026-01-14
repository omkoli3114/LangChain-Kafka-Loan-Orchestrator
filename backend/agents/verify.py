from mock_servers.crm import get_customer_by_phone
from utils.otp_manager import otp_manager

def send_otp(phone: str):
    """
    Generates and sends an OTP to the given phone number.
    """
    customer = get_customer_by_phone(phone)
    if not customer:
        # For security, we might want to pretend we sent it, but for this mock app, explicit failure is fine.
        return {"status": "FAILED", "message": "Phone number not found in our records."}
    
    otp_manager.generate_otp(phone)
    return {"status": "SUCCESS", "message": f"OTP sent to {phone}. Please enter the code."}

def verify_otp(phone: str, code: str):
    """
    Validates the OTP and returns customer details if successful.
    """
    is_valid = otp_manager.validate_otp(phone, code)
    
    if is_valid:
        customer = get_customer_by_phone(phone)
        return {
            "verified": True,
            "message": "OTP Verified Successfully.",
            "customer_id": customer["id"],
            "customer_name": customer["name"],
            # Return address for context if needed, but primary verification is done
            "address": customer["address"] 
        }
    else:
        return {
            "verified": False,
            "message": "Invalid or Expired OTP."
        }

