import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_mock_endpoints():
    print("Testing Mock Endpoints...")
    try:
        # CRM
        resp = requests.get(f"{BASE_URL}/mock/crm/customer/9876543210")
        assert resp.status_code == 200
        print("✅ Mock CRM works")
        
        # Data
        data = resp.json()
        cust_id = data['id']
        
        # Offer
        resp = requests.get(f"{BASE_URL}/mock/offer/{cust_id}")
        assert resp.status_code == 200
        print("✅ Mock Offer works")
        
        # Credit
        resp = requests.get(f"{BASE_URL}/mock/credit/{cust_id}")
        assert resp.status_code == 200
        print("✅ Mock Credit works")
        
    except Exception as e:
        print(f"❌ Mock Endpoints Failed: {e}")

def chat(session_id, message):
    resp = requests.post(f"{BASE_URL}/chat", json={
        "session_id": session_id,
        "user_id": "test_user",
        "message": message
    })
    if resp.status_code == 200:
        data = resp.json()
        reply = data['reply']
        print(f"User: {message}")
        print(f"Bot: {reply}")
        if data.get('metadata'):
            print(f"Metadata: {data['metadata']}\n")
        else:
            print("\n")
        return reply
    else:
        print(f"❌ Chat Failed: {resp.text}")
        return None

def test_case_a_instant_approval():
    print("--- Test Case A: Instant Approval ---")
    session_id = f"sess_a_{int(time.time())}"
    
    chat(session_id, "Hi, I am interested in a personal loan.")
    # Provide phone for lookup (Arjun Sharma, 9876543210, Limit 5L, Score 750)
    chat(session_id, "My phone number is 9876543210. Address is 101, Sea View Apts, Bandra West, Mumbai")
    
    # Ask for amount within limit (Limit is 500,000)
    chat(session_id, "I need 200,000 rupees.")
    
    # Confirm tenure
    chat(session_id, "For 24 months.")
    
    print("--- End Case A ---\n")

def run_tests():
    # Wait for server to start
    time.sleep(5) 
    
    test_mock_endpoints()
    test_case_a_instant_approval()
    # Add other cases if needed

if __name__ == "__main__":
    run_tests()
