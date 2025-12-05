# mcp_server.py
import sys
from fastmcp import FastMCP
from typing import List
import os

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - MCP - %(message)s',
    handlers=[logging.FileHandler('/app/logs/mcp_server.log')]
)
logger = logging.getLogger(__name__)

logger.info("MCP server started. si fcsb e top")

# Initialize the MCP server
mcp = FastMCP("Server_System_Administrator_Mihai")

@mcp.tool(description="List all files and directories in a given path")
def list_directory(dir_path: str) -> List[str]:
    logger.info("list_directory was called")  
    """
    List all files and directories in a given path.

    Args:
        dir_path (str): The directory path to list.

    Returns:
        List[str]: A list of file and directory names.
    """
    try:
        return os.listdir(dir_path)
    except FileNotFoundError:
        return [f"Directory not found: {dir_path}"]
    except PermissionError:
        return [f"Permission denied: {dir_path}"]

@mcp.tool(description="Get the content of a specified text file")
def get_file_content(file_path: str) -> str:
    """
    Get the content of a specified text file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file as a string.
    """
    try:
        logger.info("get file content a fost apelat") 
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except UnicodeDecodeError:
        return f"Cannot read file (non-text content): {file_path}"
    except PermissionError:
        return f"Permission denied: {file_path}"

if __name__ == "__main__": 
    logger.info("Starting MCP server via SSE transport on port 8000")
    mcp.run(transport="sse", port=8000, host="0.0.0.0")
