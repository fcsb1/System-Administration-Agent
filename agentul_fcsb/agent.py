# multi_tool_agent/agent.py
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm
import logging
logging.basicConfig(level=logging.DEBUG)

# path MCP server script
MCP_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "mcp_server.py")

server_params = StdioServerParameters(
    command="python", #command for running the mcp_server.
    args=["-u",MCP_SCRIPT]
)

stdio_params = StdioConnectionParams(
    server_params=server_params
)

mcp_toolset = MCPToolset(connection_params=stdio_params)


root_agent = LlmAgent(
    name="System_Administrator_Mihai",
    model=LiteLlm(
        model="ollama_chat/qwen3:14b",    # The model's name
        api_base="http://localhost:11434" # The server's address
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

ROOT_AGENT = root_agent
