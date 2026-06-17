import sys
from pathlib import Path
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# This dynamically finds the root folder: 'soc-investigation-platform'
BASE_DIR = Path(__file__).parent.parent.resolve()

class MCPHub:
    def __init__(self):
        self.sessions = {} 
        self.stack = AsyncExitStack() 

    async def connect_server(self, name: str, relative_script_path: str):
        """Connects to a single MCP server using its absolute path."""
        # Combine the root folder with the relative path to get the exact location
        abs_path = str(BASE_DIR / relative_script_path)
        
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[abs_path]
        )
        
        transport_context = stdio_client(server_params)
        read_stream, write_stream = await self.stack.enter_async_context(transport_context)
        
        session_context = ClientSession(read_stream, write_stream)
        session = await self.stack.enter_async_context(session_context)
        
        await session.initialize()
        self.sessions[name] = session
        print(f"[+] Successfully connected to {name} MCP Server")

    async def connect_all(self):
        print("Initializing MCP Hub connections...")
        # Now we specify paths relative to the root 'soc-investigation-platform' folder
        await self.connect_server("Employee", "mcp-servers/employee-mcp/server.py")
        await self.connect_server("ThreatIntel", "mcp-servers/threat-intel-mcp/server.py")
        await self.connect_server("IncidentHistory", "mcp-servers/incident-history-mcp/server.py")
        await self.connect_server("LoginHistory", "mcp-servers/login-mcp/server.py")
        
        # --- NEW TICKETING SYSTEM ADDED HERE ---
        await self.connect_server("TicketingSystem", "backend/ticketing_server.py")
        

    async def cleanup(self):
        await self.stack.aclose()
        print("[-] MCP Hub connections closed.")

mcp_hub = MCPHub()