from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Login-History-MCP")

@mcp.tool()
def check_login_history(username: str, ip_address: str = None) -> str:
    """Check the recent login history for a specific employee."""
    login_logs = {
        "rahul": [
            {"timestamp": "2026-06-16T08:00:00Z", "ip": "115.9.12.44", "location": "Chennai, India", "status": "SUCCESS"}
        ]
    }
    username = username.lower()
    if username not in login_logs:
        return f"No login history found for user: {username}"
    logs = login_logs[username]
    if ip_address:
        used_before = any(log["ip"] == ip_address for log in logs)
        if not used_before:
            return f"ANOMALY: User {username} has NEVER logged in from IP {ip_address} before. Recent logins: {logs[0]['location']}."
    return f"Recent logins for {username}: {logs}"

if __name__ == "__main__":
    mcp.run()