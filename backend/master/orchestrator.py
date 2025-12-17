import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
from agents import sales, verify, underwriting, sanction
from mock_servers import crm, offer, credit

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Fallback to checking the parent directory .env if not found
    load_dotenv() 
    api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Client
client = None
if api_key:
    client = genai.Client(api_key=api_key)

# Session storage
sessions = {}

# System Instruction
SYSTEM_INSTRUCTION = """
You are an expert NBFC Personal Loan Sales Executive. 
Your goal is to persuasively sell personal loans to customers while accurate validating their eligibility.
You must be friendly, professional, and convincing. Use natural language.

You have access to the following tools/functions:
1. `validate_customer(phone, address)`: Verifies customer KYC.
2. `check_offer(customer_id)`: Checks pre-approved limit.
3. `negotiate_terms(amount, limit)`: Returns interest rate terms.
4. `evaluate_application(credit_score, amount, limit, salary)`: Underwrites the loan.
5. `generate_sanction_letter(name, amount, tenure, rate)`: Generates the final letter.

Process:
1. Greet the customer and ask for their Phone Number to verify their account.
2. Call `validate_customer`. If failed, ask again or reject nicely.
3. If verified, call `check_offer` to see their limit.
4. Inform them of their pre-approved limit enthusiastically. Ask how much they need.
5. Once they state an amount, Call `negotiate_terms`.
   - If terms are base rate (12%), pitch it as a special offer.
   - If higher rate (14%), justify it (e.g., higher risk/amount).
6. Ask for the tenure (in months).
7. Perform underwriting using `evaluate_application`. You need the credit score (call internal mock data or ask user? The system has mock credit data).
   - Actually, you should look up their credit score using `get_credit_score` (internal tool) before underwriting.
   - If `evaluate_application` returns REQUEST_SALARY_SLIP, ask the user to upload their salary slip.
   - If REJECT, explain politely.
   - If APPROVE, proceed.
8. If Approved, confirm final details and call `generate_sanction_letter`.
9. Send the letter and close the sale.

Always maintain context. Remember what the user said.
"""

# Tools Helper
# The new SDK creates tools from functions automatically cleanly.
tool_functions = [
    verify.verify_kyc,
    offer.get_offer,
    credit.get_credit_score,
    sales.negotiate_loan,
    underwriting.evaluate_loan,
    sanction.generate_sanction
]

class ChatSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.customer_data = {}
        
        # Configure Chat with Tools
        self.chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=tool_functions,
                temperature=0.7
            )
        )

    def process_message(self, message: str, attachment_path: str = None):
        prompt = message
        if attachment_path:
            # If a file was uploaded, we tell the LLM
            # Extract salary from filename for mock logic
            from utils.file_upload import extract_salary_from_filename
            salary = extract_salary_from_filename(attachment_path)
            self.customer_data['salary'] = salary
            prompt += f"\n[SYSTEM: User uploaded salary slip. Extracted Salary: {salary}]"
        
        response = self.chat.send_message(prompt)
        return response.text

def get_or_create_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = ChatSession(session_id)
    return sessions[session_id]
