from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Employee-MCP")

@mcp.tool()
def get_employee_info(username: str) -> str:
    """Fetch the employment status, department, and location for a given user."""
    if username.lower() == "rahul":
        return "Employee: Rahul | Department: Engineering | Location: India | Status: Active"
    else:
        return f"Employee {username} not found in HR database."

if __name__ == "__main__":
    mcp.run()