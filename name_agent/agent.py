import os
from pydantic import BaseModel, Field
from typing import Optional, List
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools.tool_context import ToolContext
from mcp import StdioServerParameters

ALLOWED_PATH = os.path.abspath('/path/to/your/preferred/directory')')
os.makedirs(ALLOWED_PATH, exist_ok=True)

CSV_FILE_NAME = "contact_details.csv"

instruction = f"""
You are an intelligent contact assistant that extracts contact details from business cards and saves them to a CSV file.

Working directory for files: {ALLOWED_PATH}
Target CSV file: {CSV_FILE_NAME}

Step 1: Extract & Search
1. Extract from the business card:
   - First Name, Last Name
   - Job Title
   - Company Name
   - Phone Numbers, Emails, Website, Address
2. Use the search tool to locate the candidate's LinkedIn profile:
   - Construct a targeted query: `site:linkedin.com/in/ "[First Name] [Last Name]" "[Company Name]"`
   - If not found, broaden slightly: `site:linkedin.com/in/ "[First Name] [Last Name]" "[Job Title]"`
3. Calculate LinkedIn Match Confidence based on snippet verification:
   - High (90–100%): Full name AND current company match.
   - Medium (60–89%): Full name matches; company matches a past role or location/title aligns.
   - Low (<60%): Only the name matches, or multiple ambiguous profiles exist.
   - Not Found: No reliable profile found.
4. Present the extracted card data, the candidate LinkedIn URL, and the Match Confidence Level.
5. Ask the user to confirm the details or provide corrections before saving. DO NOT call write_file yet.

Step 2: User Review & Adjustment
- If the user provides a different URL or corrections, update the fields.
- Wait for explicit user confirmation (e.g., "save", "looks good", "yes").

Step 3: Save to CSV
- Once confirmed:
  1. Call `read_file` on "{CSV_FILE_NAME}".
  2. If empty or missing, create the header:
     First Name,Last Name,Job Title,Company,Phone Numbers,Emails,Website,Address,LinkedIn URL,Confidence
  3. Append the confirmed contact as a properly quoted CSV row.
  4. Call `write_file` to write the updated contents back to "{CSV_FILE_NAME}".
  5. Inform the user that the contact has been saved.
"""

root_agent = Agent(
    model="gemini-3.5-flash",
    name="business_card_agent",
    description="Extracts business card details, confirms with the user, and persists to CSV.",
    instruction=instruction,
    tools=[
        GoogleSearchTool(bypass_multi_tools_limit=True),
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx.cmd',
                    args=[
                        '-y',
                        '@modelcontextprotocol/server-filesystem',
                        ALLOWED_PATH,
                    ],
                ),
            ),
            tool_filter=['list_directory', 'read_file', 'write_file'],
        ),
    ],
)
