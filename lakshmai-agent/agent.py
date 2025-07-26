# ./adk_agent_samples/mcp_agent/agent.py
import os # Required for path operations
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.tools import VertexAiSearchTool, agent_tool, google_search
from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

TARGET_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/")

# DATASTORE_ID = "projects/YOUR_PROJECT_ID/locations/global/collections/default_collection/dataStores/YOUR_DATASTORE_ID"

def read_instruction(file_name):
    path = os.path.join(os.path.dirname(__file__), "instructions", file_name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

analystics_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction=read_instruction("FinAnalyticsAgent.txt"),
    tools=[google_search],
)

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='filesystem_assistant_agent',
    instruction=read_instruction("Agent.txt"),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "mcp-remote",  # Argument for npx to auto-confirm install
                    "http://localhost:8080/mcp/stream",
                    os.path.abspath(TARGET_FOLDER_PATH),
                ],
            ),
        ),
        agent_tool.AgentTool(agent=analystics_agent)
    # [VertexAiSearchTool(data_store_id=DATASTORE_ID)]
    ],
)