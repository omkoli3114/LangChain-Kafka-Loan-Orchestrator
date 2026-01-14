from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from master.orchestrator import get_or_create_session
from utils.file_upload import save_salary_slip
from mock_servers import crm, offer, credit
from agents import sales, verify, underwriting, sanction

app = FastAPI(title="NBFC Chatbot Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    message: str
    requested_amount: Optional[float] = None
    tenure_months: Optional[int] = None

class ChatResponse(BaseModel):
    reply: str
    next_action: Optional[str] = None
    metadata: Optional[dict] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session = get_or_create_session(request.session_id)
    
    # Simple logic: If user sends explicit amount/tenure, update session context separately?
    # For now, we trust the message contains the intent, as per "Conversational Master Agent" goal.
    
    try:
        reply = session.process_message(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        print(f"Error processing message: {e}")
        return ChatResponse(reply="I apologize, but I'm currently facing some technical difficulties. Please try again later.", metadata={"error": str(e)})

@app.post("/upload/salary_slip")
async def upload_salary(
    file: UploadFile = File(...), 
    session_id: str = Form(...)
):
    try:
        file_path = save_salary_slip(file, session_id)
        
        # Notify the agent about the upload
        session = get_or_create_session(session_id)
        # We inject a system message into the conversation
        sys_msg = f"User has uploaded a salary slip." 
        # Ideally we pass this file path to process_message, but let's do it via next chat or internal state?
        # The orchestrator `process_message` handles `attachment_path`.
        # But `process_message` expects a user message.
        # We can trigger a "hidden" message loop.
        
        reply = session.process_message(message="[SYSTEM: User uploaded salary slip]", attachment_path=file_path)
        
        return {"status": "success", "file_path": file_path, "agent_reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mock Endpoints (exposed as requested)

@app.get("/mock/crm/customer/{phone}")
def get_customer(phone: str):
    data = crm.get_customer_by_phone(phone)
    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return data

@app.get("/mock/offer/{customer_id}")
def get_offer_api(customer_id: str):
    return offer.get_offer(customer_id)

@app.get("/mock/credit/{customer_id}")
def get_credit_api(customer_id: str):
    return credit.get_credit_score(customer_id)

# Agent Direct Endpoints (for testing/debug)

@app.get("/agent/otp/send")
def agent_otp_send(phone: str):
    return verify.send_otp(phone)

@app.get("/agent/otp/verify")
def agent_otp_verify(phone: str, code: str):
    return verify.verify_otp(phone, code)

@app.get("/agent/sales")
def agent_sales(amount: float, limit: float):
    return sales.negotiate_loan(amount, limit)

@app.get("/agent/underwrite")
def agent_underwrite(score: int, amount: float, limit: float, salary: float = 0):
    return underwriting.evaluate_loan(score, amount, limit, salary)

@app.post("/agent/sanction")
def agent_sanction(name: str, amount: float, tenure: int, rate: float):
    return sanction.generate_sanction(name, amount, tenure, rate)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
