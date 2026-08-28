import asyncio
import json
import re
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class StudyAgent:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["server.py"]
        )
        self.allowed_tools = {
            "explain_topic": {"params": ["topic"], "description": "Explain a topic in simple terms"},
            "create_study_plan": {"params": ["topic", "days"], "description": "Create a study plan for a topic over N days"},
            "generate_revision_checklist": {"params": ["topic"], "description": "Generate a revision checklist for a topic"}
        }
    
    def parse_request(self, user_request: str) -> dict:
        """Parse user request to determine tool and arguments."""
        request_lower = user_request.lower()
        
        if "explain" in request_lower or "what is" in request_lower or "define" in request_lower:
            topic_match = re.search(r'(explain|what is|define)\s+(.+)', request_lower)
            if topic_match:
                topic = topic_match.group(2).strip().rstrip('?')
                return {"tool": "explain_topic", "args": {"topic": topic}}
        
        elif "study plan" in request_lower or "plan to study" in request_lower or "schedule" in request_lower:
            topic_match = re.search(r'(study plan|plan to study|schedule)\s+(?:for\s+)?(.+)', request_lower)
            days_match = re.search(r'(\d+)\s*days?', request_lower)
            if topic_match:
                topic = topic_match.group(2).strip().rstrip('?')
                days = int(days_match.group(1)) if days_match else 7
                return {"tool": "create_study_plan", "args": {"topic": topic, "days": days}}
        
        elif "checklist" in request_lower or "revision" in request_lower or "review" in request_lower:
            topic_match = re.search(r'(checklist|revision|review)\s+(?:for\s+)?(.+)', request_lower)
            if topic_match:
                topic = topic_match.group(2).strip().rstrip('?')
                return {"tool": "generate_revision_checklist", "args": {"topic": topic}}
        
        return {"tool": None, "args": {}, "error": "Could not determine appropriate tool for request"}
    
    def validate_tool(self, tool_name: str) -> bool:
        """Validate that the tool is allowed."""
        return tool_name in self.allowed_tools
    
    def validate_args(self, tool_name: str, args: dict) -> tuple[bool, str]:
        """Validate tool arguments."""
        if tool_name not in self.allowed_tools:
            return False, f"Tool '{tool_name}' is not allowed"
        
        required_params = self.allowed_tools[tool_name]["params"]
        for param in required_params:
            if param not in args:
                return False, f"Missing required parameter: {param}"
            if param == "topic" and (not args[param] or not str(args[param]).strip()):
                return False, "Topic cannot be empty"
            if param == "days" and (not isinstance(args[param], int) or args[param] < 1 or args[param] > 14):
                return False, "Days must be an integer between 1 and 14"
        
        return True, "Valid"
    
    async def execute(self, user_request: str) -> dict:
        """Execute the agent workflow: parse, validate, call tool."""
        print(f"\n{'='*60}")
        print(f"Agent Demo: Processing request: '{user_request}'")
        print(f"{'='*60}")
        
        parsed = self.parse_request(user_request)
        
        if not parsed["tool"]:
            print(f"[ERROR] Error: {parsed.get('error', 'Unknown error')}")
            return {"success": False, "error": parsed.get('error')}
        
        print(f"[OK] Parsed request -> Tool: {parsed['tool']}, Args: {parsed['args']}")
        
        if not self.validate_tool(parsed["tool"]):
            print(f"[ERROR] Error: Tool '{parsed['tool']}' is not allowed")
            return {"success": False, "error": f"Tool '{parsed['tool']}' is not allowed"}
        
        print(f"[OK] Tool '{parsed['tool']}' is allowed")
        
        valid, msg = self.validate_args(parsed["tool"], parsed["args"])
        if not valid:
            print(f"[ERROR] Validation failed: {msg}")
            return {"success": False, "error": msg}
        
        print(f"[OK] Arguments validated: {msg}")
        
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print(f"[TOOL] Calling tool '{parsed['tool']}' with args: {parsed['args']}")
                result = await session.call_tool(parsed["tool"], parsed["args"])
                
                print(f"[OK] Tool executed successfully")
                print(f"\nResult:")
                print(result.content[0].text)
                
                return {"success": True, "result": result.content[0].text}


async def main():
    agent = StudyAgent()
    
    test_requests = [
        "Explain what is Python",
        "Create a study plan for machine learning for 10 days",
        "Generate a revision checklist for FastAPI",
        "What is MCP?",
        "Plan to study Git for 3 days",
        "Review checklist for Python"
    ]
    
    print("=" * 60)
    print("Study Agent Demonstration")
    print("=" * 60)
    print("This agent parses natural language requests, validates the")
    print("selected tool and arguments, then executes the tool via MCP.")
    
    for request in test_requests:
        await agent.execute(request)
    
    print("\n" + "=" * 60)
    print("Agent demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())