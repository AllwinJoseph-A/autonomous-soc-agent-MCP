from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database.database import engine
from database import models
from mcp_hub import mcp_hub
from agent import investigation_agent
import ollama

# Physically create the database tables
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Phase: Connect to all MCP servers
    await mcp_hub.connect_all()
    yield 
    # Shutdown Phase: Cleanly disconnect
    await mcp_hub.cleanup()

app = FastAPI(
    title="Autonomous SOC Investigation Platform",
    description="Enterprise API for automated security triage using MCP and LLMs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration so React can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "operational", "mcp_connections": list(mcp_hub.sessions.keys())}

@app.get("/test-llm")
def test_local_llm():
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {
                'role': 'user', 
                'content': 'You are an elite SOC Analyst. Reply with exactly one sentence: "Local AI Brain is online and ready for triage."'
            }
        ])
        return {"status": "success", "llm_response": response['message']['content']}
    except Exception as e:
        return {"status": "error", "message": f"Is Ollama running? Error: {str(e)}"}

@app.get("/tools")
async def view_agent_tools():
    tools = await investigation_agent.get_all_tools()
    return {"total_tools": len(tools), "tools": tools}

# --- THIS IS THE CLASS FASTAPI WAS LOOKING FOR ---
class AlertPayload(BaseModel):
    message: str

@app.post("/investigate")
async def trigger_investigation(alert: AlertPayload):
    """Simulate receiving an alert from a SIEM and trigger the AI Agent."""
    agent_result = await investigation_agent.investigate(alert.message)
    return {
        "original_alert": alert.message,
        "investigation_report": agent_result["report"],
        "evidence": agent_result["evidence"]  
    }