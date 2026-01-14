# Capital Connect - NBFC Sales AI Agent

Capital Connect is an intelligent, agentic AI-powered Personal Loan Sales Executive designed for Non-Banking Financial Companies (NBFCs). It uses a Master-Worker agent architecture to orchestrate conversations, negotiate loan terms, verify customer identity (KYC), underwrite loans in real-time, and generate sanction letters.

## 🚀 Key Features

*   **Conversational Sales**: A persuasive AI implementation (Master Agent) that negotiates interest rates based on loan limits.
*   **Agentic Workflow**: Specialized worker agents for specific tasks:
    *   **Sales Agent**: Negotiates terms using business logic (12% vs 14% interest rates).
    *   **Verification Agent**: Handles OTP generation and validation using a mock CRM.
    *   **Underwriting Agent**: Evaluates credit scores and financial eligibility (EMI vs Salary ratio).
    *   **Sanction Agent**: Generates official PDF sanction letters instantly.
*   **Real-time Event Streaming**: Captures and processes agent actions using Kafka and Flink.
*   **Mock Infrastructure**: Includes fully functional mock servers for CRM, Credit Bureau, and Offer Engine.
*   **Modern Frontend**: A responsive chat interface built with React, Vite, and TailwindCSS.

## 🛠️ Architecture

The system follows a micro-service inspired architecture:

1.  **Backend (FastAPI)**: Hosts the AI Orchestrator, Agents, and Mock API endpoints.
2.  **Frontend (React)**: User-facing chat interface for customers.
3.  **Streaming (Kafka & Flink)**: Asynchronous event logging for audit and analytics.
4.  **AI Engine**: Powered by Google Gemini 2.5 Flash for natural language understanding and tool calling.

## 📦 Prerequisites

*   Python 3.10+
*   Node.js 18+
*   Docker & Docker Compose (for Kafka/Flink)
*   Google Gemini API Key

## ⚡ Quick Start

### 1. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment and activate it:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables:
Create a `.env` file in the root or `backend/` directory and add your key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Run the backend server:

```bash
uvicorn app:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```
The application will be running at `http://localhost:5173`.

### 3. Infrastructure (Optional)

To run the Kafka and Flink streaming components:

```bash
cd infra
# Ensure you have a docker-compose.yml file here
docker-compose up -d
```

## 🧪 Testing the Flow

1.  Open the frontend in your browser.
2.  Start a conversation (e.g., "Hi, I'm looking for a loan").
3.  The agent will ask for your phone number. Use one of the test numbers from `backend/data/customers.json` (e.g., `9307666607`, `9876543210`).
4.  Enter the OTP (simulated, any 4-digit code usually works in dev mode unless strict checking is enabled).
5.  Negotiate the loan amount and tenure.
6.  If required (loan > 2x limit), upload a dummy salary slip image.
7.  Receive your Sanction Letter PDF!

## 📂 Project Structure

```
capital-connect/
├── backend/
│   ├── agents/          # Worker agents (logic for sales, underwriting, etc.)
│   ├── master/          # Orchestrator (LLM integration)
│   ├── mock_servers/    # Mock APIs for CRM, Credit, Offers
│   ├── streaming/       # Flink jobs
│   ├── data/            # Dummy customer data
│   └── app.py           # Main FastAPI entry point
├── frontend/            # React application
└── infra/               # Infrastructure configuration
```
