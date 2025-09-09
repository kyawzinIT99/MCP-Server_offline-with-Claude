# Import necessary libraries
import os
import json
from typing import List, Dict, Any

# MCP libraries for connecting to server
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Anthropic API for Claude
#from anthropic import Anthropic

# Set up Anthropic API key (using the one you provided)
#os.environ["ANTHROPIC_API_KEY"] = "your_anthropic_api_key_here"

# Initialize the Anthropic client
#client = Anthropic()

# Path to your MCP server
mcp_server_path = "/Users/berry/Desktop/MCP/mcp-crypto-server"
print("Setup complete!")
