import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 60)
            print("MCP Study Tools Server - Client Test")
            print("=" * 60)
            
            print("\n[1] Listing available tools...")
            tools_result = await session.list_tools()
            print(f"Found {len(tools_result.tools)} tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            print("\n[2] Listing available resources...")
            resources_result = await session.list_resources()
            print(f"Found {len(resources_result.resources)} resources:")
            for resource in resources_result.resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            print("\n[3] Reading project://course-outline resource...")
            course_outline = await session.read_resource("project://course-outline")
            print(course_outline.contents[0].text)
            
            print("\n[4] Reading project://status resource...")
            status = await session.read_resource("project://status")
            print(status.contents[0].text)
            
            print("\n[5] Calling explain_topic tool with 'python'...")
            explain_result = await session.call_tool("explain_topic", {"topic": "python"})
            print(explain_result.content[0].text)
            
            print("\n[6] Calling create_study_plan tool with topic='machine learning', days=5...")
            study_plan_result = await session.call_tool("create_study_plan", {"topic": "machine learning", "days": 5})
            print(study_plan_result.content[0].text)
            
            print("\n[7] Calling generate_revision_checklist tool with 'fastapi'...")
            checklist_result = await session.call_tool("generate_revision_checklist", {"topic": "fastapi"})
            print(checklist_result.content[0].text)
            
            print("\n[8] Testing error handling - empty topic for explain_topic...")
            error_result = await session.call_tool("explain_topic", {"topic": ""})
            print(error_result.content[0].text)
            
            print("\n[9] Testing clamping - create_study_plan with days=20 (should clamp to 14)...")
            clamp_result = await session.call_tool("create_study_plan", {"topic": "git", "days": 20})
            print(clamp_result.content[0].text)
            
            print("\n" + "=" * 60)
            print("Client test completed successfully!")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())