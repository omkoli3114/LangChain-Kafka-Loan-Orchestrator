import random
import time
import logging

# Configure logging to ensure OTPs appear in console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OTPManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OTPManager, cls).__new__(cls)
            cls._instance.otps = {} # {phone: {"code": str, "expiry": float}}
        return cls._instance

    def generate_otp(self, phone: str, expiry_seconds: int = 300) -> str:
        """Generates a 6-digit OTP, stores it with expiry, and 'sends' it via console."""
        code = f"{random.randint(0, 999999):06d}"
        expiry = time.time() + expiry_seconds
        
        self.otps[phone] = {
            "code": code,
            "expiry": expiry
        }
        
        self._send_otp(phone, code)
        return code

    def _send_otp(self, phone: str, code: str):
        """Simulates sending OTP via SMS by logging it to the console."""
        message = f"========================================\n[SMS] To {phone}: Your OTP is {code}\n========================================"
        print(message)
        logger.info(message) # Ensure it hits logs

    def validate_otp(self, phone: str, code: str) -> bool:
        """Validates the OTP. Checks existence, equality, and expiry."""
        if phone not in self.otps:
            return False
            
        record = self.otps[phone]
        
        if time.time() > record["expiry"]:
            del self.otps[phone] # Cleanup expired
            return False
            
        if record["code"] == code:
            del self.otps[phone] # Consumed
            return True
            
        return False

# Global instance
otp_manager = OTPManager()
