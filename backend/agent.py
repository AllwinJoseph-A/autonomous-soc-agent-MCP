import ollama
from mcp_hub import mcp_hub

class InvestigationAgent:
    def __init__(self):
        # We map tool names to server names so we know exactly which MCP server to call
        self.tool_server_map = {}

    async def get_formatted_tools(self):
        """Fetches tools from MCP servers and formats them exactly how Ollama expects."""
        ollama_tools = []
        for server_name, session in mcp_hub.sessions.items():
            tool_response = await session.list_tools()
            for tool in tool_response.tools:
                self.tool_server_map[tool.name] = server_name
                # Convert MCP schema to Ollama/OpenAI tool format
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
        return ollama_tools

    async def investigate(self, alert_text: str):
        print(f"\n[AGENT] Starting investigation for: {alert_text}")
        tools = await self.get_formatted_tools()
        evidence_log = [] # <-- NEW: We will store the AI's actions here
        
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are an elite Autonomous SOC Analyst. You are evaluating a security alert. "
                    "CRITICAL RULES: "
                    "1. You MUST use your available tools to investigate the user and the IP address. "
                    "2. DO NOT hallucinate, guess, or make up information about IP addresses, DNS records, or employee data. "
                    "3. If you do not know something, you MUST call a tool to find out. "
                    "4. Gather evidence using tools first, then provide a final verdict. "
                    "5. If you determine the alert is a TRUE POSITIVE critical threat, you MUST use the create_incident_ticket tool to escalate it." # <-- NEW RULE
                )
            },
            {"role": "user", "content": alert_text}
        ]

        response = ollama.chat(model='llama3.2', messages=messages, tools=tools)
        messages.append(response['message'])
        
        if not response['message'].get('tool_calls'):
            return {
                "report": response['message']['content'],
                "evidence": [{"tool": "None", "details": "The LLM decided no tools were required."}]
            }

        # Execute tools and log the evidence
        for tool_call in response['message']['tool_calls']:
            func_name = tool_call['function']['name']
            func_args = tool_call['function']['arguments']
            
            server_name = self.tool_server_map[func_name]
            session = mcp_hub.sessions[server_name]
            
            result = await session.call_tool(func_name, func_args)
            tool_output = result.content[0].text
            
            # --- NEW: Record exactly what happened ---
            evidence_log.append({
                "tool": func_name,
                "server": server_name,
                "details": tool_output
            })
            # -----------------------------------------
            
            messages.append({
                "role": "tool",
                "content": tool_output,
                "name": func_name
            })
        
        final_response = ollama.chat(model='llama3.2', messages=messages)
        
        # --- NEW: Return BOTH the report and the log ---
        return {
            "report": final_response['message']['content'],
            "evidence": evidence_log
        }
        
        # Step 1: System Prompt & Initial Request
        # Step 1: System Prompt & Initial Request (HARDENED)
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are an elite Autonomous SOC Analyst. You are evaluating a security alert. "
                    "CRITICAL RULES: "
                    "1. You MUST use your available tools to investigate the user and the IP address. "
                    "2. DO NOT hallucinate, guess, or make up information about IP addresses, DNS records, or employee data. "
                    "3. If you do not know something, you MUST call a tool to find out. "
                    "4. Gather evidence using tools first, then provide a final verdict."
                )
            },
            {"role": "user", "content": alert_text}
        ]

        # Step 2: Let the AI decide if it needs tools
        print("[AGENT] Asking LLM for initial assessment...")
        response = ollama.chat(model='llama3.2', messages=messages, tools=tools)
        messages.append(response['message'])
        
        # Step 3: Did the AI ask to use any tools?
        if not response['message'].get('tool_calls'):
            print("[AGENT] LLM decided no tools were needed.")
            return response['message']['content']

        # Step 4: Execute the tools requested by the AI
        for tool_call in response['message']['tool_calls']:
            func_name = tool_call['function']['name']
            func_args = tool_call['function']['arguments']
            print(f"[AGENT] Executing Tool: {func_name} with args {func_args}")
            
            # Find the correct MCP server and execute the tool
            server_name = self.tool_server_map[func_name]
            session = mcp_hub.sessions[server_name]
            
            # Call the tool via the MCP protocol
            result = await session.call_tool(func_name, func_args)
            
            # Step 5: Feed the tool's result back into the AI's memory
            tool_output = result.content[0].text
            print(f"[{server_name}] returned: {tool_output}")
            
            messages.append({
                "role": "tool",
                "content": tool_output,
                "name": func_name
            })
        
        # Step 6: Get the final report from the AI now that it has the evidence
        print("[AGENT] Evidence gathered. Generating final report...")
        final_response = ollama.chat(model='llama3.2', messages=messages)
        return final_response['message']['content']

# Global instance
investigation_agent = InvestigationAgent()