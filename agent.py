# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from tools import tools, schedule_event
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class SalesCallAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",  # or use "llama3-70b-8192"
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent="chat-conversational-react-description",
            memory=self.memory,
            verbose=True
        )

    def process_transcription(self, transcription: str) -> dict:
        """
        Process the transcription and let the agent use tools to generate summary, action items, and take actions.
        Returns a dict with keys: summary, action_items, calendar, web_search
        """
        try:
            # Prompt construction
            prompt = (
                """
                You are an expert AI sales assistant. Analyze the following sales call transcription and:
                1. Provide a concise executive summary
                2. Extract a list of specific action items
                3. If a meeting/demo/follow-up is mentioned or needed:
                - ALWAYS use the Calendar tool to schedule it
                - Format the date and time EXACTLY like this: 2025-06-26T14:00:00
                - Include a clear summary of what the meeting is about
                - Example Calendar tool usage: schedule_event("Sales Demo Follow-up", "2025-06-26T14:00:00")
                4. If a competitor, product, or market trend is mentioned, use the Web Search tool to find relevant info
                5. Always use the Web Search tool if a company, product, or service is mentioned. Don't assume prior knowledge—look it up.
                IMPORTANT CALENDAR INSTRUCTIONS:
                - If any meeting, demo, or follow-up is discussed, you MUST schedule it
                - Always use ISO 8601 format for dates (YYYY-MM-DDTHH:MM:SS)
                - The Calendar section of your response should only contain the result from the Calendar tool
                - Do not include any other text in the Calendar section

                IMPORTANT WEB SEARCH INSTRUCTIONS:
                - If you use the Web Search tool, include the search results in the 'Web Search' section
                - Format the 'Web Search' section as a list of links and short descriptions

                Return your results in this format:
                Executive Summary: ...
                Action Items: ...
                Calendar: ...
                Web Search: ...

                Here is the transcription:
                """ + transcription
            )

            result = self.agent.run(prompt)

            output = {
                "summary": "",
                "action_items": [],
                "calendar": "",
                "web_search": ""
            }

            def extract_section(label: str) -> str:
                pattern = rf"{label}:\s*(.*?)(?=\n[A-Z][a-z]+:|$)"
                match = re.search(pattern, result, re.DOTALL)
                return match.group(1).strip() if match else ""

            # Extract sections
            output["summary"] = extract_section("Executive Summary")

            action_items_raw = extract_section("Action Items")
            if action_items_raw:
                output["action_items"] = [
                    item.strip("-• \n") for item in action_items_raw.splitlines() if item.strip()
                ]

            output["calendar"] = extract_section("Calendar")
            output["web_search"] = extract_section("Web Search")

            # If the agent *described* a calendar event but didn’t actually call the tool, try scheduling it
            if output["calendar"] and "Event created:" not in output["calendar"] and "http" not in output["calendar"]:
                date_match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", output["calendar"])
                if date_match:
                    date_str = date_match.group(0)
                    # Remove the date from calendar string to isolate summary
                    summary_text = output["calendar"].replace(date_str, "").strip(' :.\n') or "Follow-up Meeting"
                    scheduled = schedule_event(summary_text, date_str)
                    output["calendar"] = scheduled

            return output

        except Exception as e:
            raise Exception(f"Failed to process transcription with agent: {str(e)}")
