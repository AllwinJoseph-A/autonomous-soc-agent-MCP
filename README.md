
# autonomous-soc-agent-MCP
# Autonomous SOC Investigation Platform

An AI-driven Security Operations Center (SOC) platform that utilizes local LLMs and the Model Context Protocol (MCP) to autonomously triage, investigate, and escalate security alerts.

## 🚀 Architecture
* **Frontend:** React / Vite (Dashboard UI)
* **Backend:** FastAPI (Highly concurrent orchestration)
* **AI Engine:** Local Llama 3.2 (via Ollama) ensuring strict enterprise data sovereignty.
* **Microservices:** Custom MCP servers connecting the reasoning engine to enterprise databases (Threat Intel, HR, Login History).

## 🧠 Core Capabilities
* **Zero-Shot Semantic Triage:** Parses raw, unlabeled SIEM alerts to identify actors, IPs, and attack vectors.
* **Autonomous Tool Orchestration:** Uses ReAct logic to dynamically query mocked HR and Threat Intelligence databases to build context.
* **Automated Escalation:** Evaluates evidence and writes structured JSON incident tickets directly to the filesystem for True Positive threats.

## 🛠️ How to Run Locally
1. **Start the Frontend:** `cd frontend && npm run dev`
2. **Start the Backend Hub:** `cd backend && source venv/bin/activate && uvicorn main:app --reload`
3. **Ensure Ollama is running** with `llama3.2` pulled.
 23cf09d (Initial commit: Autonomous SOC Platform with MCP architecture)
