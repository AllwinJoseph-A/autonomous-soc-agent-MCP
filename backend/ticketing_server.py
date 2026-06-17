import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize the MCP Server
mcp = FastMCP("TicketingSystem")

# Ensure a 'tickets' folder exists on your hard drive
os.makedirs("tickets", exist_ok=True)

@mcp.tool()
def create_incident_ticket(title: str, severity: str, target_user: str, target_ip: str, investigation_summary: str) -> str:
    """
    Creates a formal security incident ticket as a JSON file.
    Use this tool ONLY when an investigation confirms a TRUE POSITIVE threat that requires human intervention.
    """
    # Generate a unique ticket ID based on the current time
    ticket_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # BULLETPROOFING: Force the LLM's inputs to be strings so .upper() never crashes
    safe_severity = str(severity).upper() if severity else "CRITICAL"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "timestamp": datetime.now().isoformat(),
        "title": str(title),
        "severity": safe_severity,
        "target_user": str(target_user),
        "target_ip": str(target_ip),
        "investigation_summary": str(investigation_summary),
        "status": "OPEN",
        "assigned_team": "Incident Response"
    }
    
    filepath = f"tickets/{ticket_id}.json"
    
    # Write the ticket to the hard drive
    try:
        with open(filepath, "w") as f:
            json.dump(ticket_data, f, indent=4)
        return f"SUCCESS: Incident Ticket {ticket_id} has been successfully generated and saved to disk."
    except Exception as e:
        return f"ERROR: Failed to write ticket to disk. Reason: {str(e)}"

if __name__ == "__main__":
    mcp.run()