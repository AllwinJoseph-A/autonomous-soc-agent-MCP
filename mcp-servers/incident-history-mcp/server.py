from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Incident-History-MCP")

@mcp.tool()
def get_incident_history(ip_address: str) -> str:
    """Query the enterprise incident management system for past security events."""
    past_incidents = {
        "103.45.67.89": "[2025-11-12] CRITICAL: Ransomware payload delivered via this IP. Status: Resolved."
    }
    if ip_address in past_incidents:
        return f"HISTORY FOUND: {past_incidents[ip_address]}"
    return f"No historical incidents found for IP {ip_address}."

if __name__ == "__main__":
    mcp.run()