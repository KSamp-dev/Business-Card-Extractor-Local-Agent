# Business Card Extraction Agent
I built this so  business executives can quickly capture contact details from a simple picture of a business card. I found tons of business cards laying around that I never had time to enter into my CRM or Connect with on LinkedIn. This allowed me to extract key contact information and find the correct Linkedin profile to connect with. The output is simple .csv file you can upload into any database. 

I built this AI agent with the **Google Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**. 

## Features

* **Intelligent Data Extraction:** Extracts names, job titles, companies, phone numbers, emails, websites, and addresses from raw business card text or images.
* **Automated LinkedIn Discovery:** Uses the `GoogleSearchTool` to automatically search for the contact on LinkedIn and calculates a "Match Confidence" score (High, Medium, Low, Not Found) based on snippet verification.
* **Human-in-the-Loop Review:** Presents the gathered information to the user for explicit confirmation or correction before any data is saved.
* **Local Filesystem Integration:** Uses the `@modelcontextprotocol/server-filesystem` via MCP to securely read, format, and append the confirmed contact details directly to a local `contact_details.csv` file.

## Prerequisites

Before running the agent, ensure you have the following installed:

* **Python 3.10+**
* **Node.js & npm** (required to run the local MCP filesystem server via `npx`)
* **Google Gemini API Key** (to power the LLM and Google Search capabilities)

## Installation & Setup

1. **Install Python Dependencies:**
   Ensure you have the Google ADK and MCP libraries installed in your environment:
   ```bash
   pip install google-adk mcp pydantic python-dotenv
   ```

2. **Set Environment Variables:**
   Create a `.env` file in your project root or set the following system environment variable:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Configure the Working Directory:**
   By default, the agent is configured to write to:
   `C:/Users`
   *(Note: You can update the `ALLOWED_PATH` variable in the script to match your preferred local directory).* 
   
   The agent will automatically create this directory if it does not exist.

## How It Works

1. **Input:** You provide the agent with the text or an image of a business card.
2. **Process:** 
   * The agent parses the standard fields.
   * It executes a targeted Google Search (`site:linkedin.com/in/ "Name" "Company"`) to find their profile.
3. **Review:** The agent outputs a summary of the extracted data alongside the LinkedIn URL and a match confidence score, asking, *"Does this look correct?"*
4. **Save:** Once you type "yes", "save", or provide corrections, the agent uses the local filesystem MCP tool to check if `contact_details.csv` exists. If not, it writes the headers. Finally, it appends the new contact as a CSV row.

## Usage

Usage

To utilize the agent's full multimodal capabilities (such as uploading photos of business cards), you will run it through the ADK web interface:

Ensure ADK is Downloaded: Verify that you have the Google ADK installed in your environment.

Navigate to the Directory: Open your terminal and navigate to the parent directory containing your name_agent folder.

Launch the Web Interface: Start the ADK web UI by running the following command:

adk web


Test the Agent: Once the web interface opens in your browser, select your agent. You can now use the multimodal chat to upload an image of a business card. The agent will process the image, search for the LinkedIn profile, ask for your confirmation, and save the data to your CSV!
