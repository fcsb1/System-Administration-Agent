# multi_tool_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.adk.models.lite_llm import LiteLlm
import logging
import os
logging.basicConfig(level=logging.DEBUG)

# Connect to MCP server via HTTP

api_key = os.environ.get("MCP_API_KEY")

sse_params = SseConnectionParams(
    url="http://mcp-server:8000/sse",
    headers={"X-API-Key": api_key}
)

mcp_toolset = MCPToolset(connection_params=sse_params)


root_agent = LlmAgent(
    name="System_Administrator_Mihai",
    model=LiteLlm(
        model="ollama_chat/qwen3:14b",    # The model's name
        api_base="http://ollama:11434", # The server's address
        temperature=0
    ),
instruction=(
        "You are a system administrator assistant.\n\n"
        "The files you manage are located in the directory: /managed_folder\n"
        "Respond naturally to all user messages.\n"
        "- For greetings, casual conversation, or general questions, respond directly without using tools.\n"
        "- ONLY use the available filesystem tools when the user specifically asks about files, "
        "directories, or file contents in the managed filesystem.\n\n"
    ),
    description="Agent that uses MCP filesystem tools (list_directory, get_file_content) when needed.",
    tools=[mcp_toolset],
)

ROOT_AGENT = root_agent
