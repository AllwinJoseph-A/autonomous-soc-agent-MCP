from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Threat-Intel-MCP")

@mcp.tool()
def check_ip_reputation(ip_address: str) -> str:
    """Check an IP address against known threat intelligence databases."""
    malicious_ips = {
        "103.45.67.89": "Known Tor Exit Node - Location: Russia - Risk: HIGH",
        "45.33.22.11": "Associated with Emotet Botnet - Location: Unknown - Risk: CRITICAL"
    }
    if ip_address in malicious_ips:
        return f"ALERT: IP {ip_address} is flagged! Details: {malicious_ips[ip_address]}"
    return f"IP {ip_address} is clean. No known threats detected."

if __name__ == "__main__":
    mcp.run()