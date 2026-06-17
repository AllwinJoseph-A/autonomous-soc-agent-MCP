# Autonomous SOC Investigation Platform

An AI-driven Security Operations Center (SOC) platform that utilizes local LLMs and the Model Context Protocol (MCP) to autonomously triage, investigate, and escalate security alerts.

---

## 🏗️ System Architecture
The platform follows a modular, agentic architecture designed for security, low latency, and data sovereignty.



* **Frontend:** React / Vite (Dashboard UI for real-time investigation and agent monitoring).
* **Backend:** FastAPI (Highly concurrent orchestration hub for managing MCP connections).
* **AI Engine:** Local Llama 3.2 (via Ollama) ensuring strict enterprise data sovereignty and avoiding cloud-based data leakage.
* **MCP Hub:** A suite of custom Model Context Protocol servers connecting the reasoning engine to isolated enterprise databases:
    * **Threat Intel:** Real-time IP reputation and threat categorization.
    * **HR Database:** Employee verification and role-based access context.
    * **Login History:** Behavioral baseline for user authentication.
    * **TicketingSystem:** Automated escalation for True Positive incidents.

## 🧠 Core Capabilities
* **Zero-Shot Semantic Triage:** Parses raw, unlabeled SIEM-style alerts to identify actors, IPs, and attack vectors.
* **Autonomous Tool Orchestration:** Uses ReAct logic to dynamically query mocked enterprise databases to build evidence-based context.
* **Automated Escalation:** Evaluates evidence and autonomously writes structured JSON incident tickets directly to the filesystem for verified security threats.
* **Explainable AI (XAI) Audit Trail:** Provides a deterministic trail of tool executions, forcing the model to verify data through database queries to eliminate hallucinations.

## 🚀 Setup & Installation

### 1. Prerequisites
* [Ollama](https://ollama.com/) installed and running.
* Pull the Llama 3.2 model: `ollama pull llama3.2`
* Python 3.10+ and Node.js 18+

### 2. Backend Orchestration
Navigate to the `backend` folder:
```bash
python -m venv venv
# Activate virtual environment
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
