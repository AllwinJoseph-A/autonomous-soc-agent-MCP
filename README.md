# Autonomous SOC Investigation Platform

An AI-driven Security Operations Center (SOC) platform that utilizes local LLMs and the Model Context Protocol (MCP) to autonomously triage, investigate, and escalate security alerts.

## 🚀 Architecture
This platform is built on an agentic architecture designed for speed, security, and local data sovereignty.

* **Frontend:** React / Vite (Dashboard UI for real-time investigation)
* **Backend:** FastAPI (Highly concurrent orchestration hub)
* **AI Engine:** Local Llama 3.2 (via Ollama) ensuring strict enterprise data sovereignty.
* **MCP Hub:** Custom Model Context Protocol servers connecting the reasoning engine to isolated enterprise databases (Threat Intel, HR, Login History, and Ticketing).

## 🧠 Core Capabilities
* **Zero-Shot Semantic Triage:** Parses raw, unlabeled SIEM-style alerts to identify actors, IPs, and attack vectors.
* **Autonomous Tool Orchestration:** Uses ReAct logic to dynamically query mocked HR and Threat Intelligence databases to build evidence-based context.
* **Automated Escalation:** Evaluates evidence and autonomously writes structured JSON incident tickets directly to the filesystem for True Positive threats.
* **Explainable AI (XAI):** Provides a deterministic audit trail of tool executions, preventing hallucinations by forcing the model to verify data through database queries.

## 🛠️ Prerequisites
* [Ollama](https://ollama.com/) installed and running with `llama3.2` pulled.
* Python 3.10+
* Node.js 18+

## 🚀 How to Run Locally

### 1. Backend Orchestration
Navigate to the `backend` folder and start the hub:
```bash
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
