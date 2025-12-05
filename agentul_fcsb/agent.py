# multi_tool_agent/agent.py
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.adk.models.lite_llm import LiteLlm
import logging
logging.basicConfig(level=logging.DEBUG)

# path MCP server script
#MCP_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "mcp_server.py")

# Connect to MCP server via HTTP
sse_params = SseConnectionParams(
    url="http://mcp-server:8000/sse"
)

mcp_toolset = MCPToolset(connection_params=sse_params)

# DEBUG: Try to list available tools
# try:
#     print("Attempting to connect to MCP server...")
#     # This should trigger the connection
#     available_tools = mcp_toolset.get_tools() if hasattr(mcp_toolset, 'get_tools') else []
#     print(f"Available tools: {available_tools}")
# except Exception as e:
#     print(f"ERROR connecting to MCP server: {e}")


root_agent = LlmAgent(
    name="System_Administrator_Mihai",
    model=LiteLlm(
        model="ollama_chat/qwen3:14b",    # The model's name
        api_base="http://ollama:11434", # The server's address
        temperature=0
    ),
instruction=(
        "You are a system administrator assistant.\n\n"
        "Respond naturally to all user messages.\n"
        "- For greetings, casual conversation, or general questions, respond directly without using tools.\n"
        "- ONLY use the available filesystem tools when the user specifically asks about files, "
        "directories, or file contents in the managed filesystem.\n\n"
    ),
    description="Agent that uses MCP filesystem tools (list_directory, get_file_content) when needed.",
    tools=[mcp_toolset],
)

# ADD THIS DEBUG CODE:
print("=" * 50)
print("REGISTERED TOOLS:")
if hasattr(root_agent, 'tools'):
    for tool in root_agent.tools:
        print(f"  - {tool}")
print("=" * 50)

ROOT_AGENT = root_agent
