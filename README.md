# AI Sales Call Assistant

An AI-powered tool that automatically transcribes sales calls, generates summaries, and identifies action items using OpenAI's Whisper and GPT-4.

## Features

- 🎙️ Audio transcription using OpenAI Whisper
- 📊 AI-powered call analysis and summarization
- ✅ Automatic action item extraction
- 🌐 Real-time web search via SerpAPI
- 📅 Google Calendar integration for scheduling meetings
- 🎯 Clean Streamlit interface
- 🐳 Dockerized for easy deployment

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- SerpAPI key (for web search)
- Google Cloud project with Calendar API enabled
- Docker (for containerized deployment)

## Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-sales-call-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key, SerpAPI key, and any other required variables.

5. Run the application:
```bash
streamlit run app.py
```

## Advanced Features & Integrations

### Google Calendar Integration

- **Setup:**
  1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials) and create OAuth 2.0 credentials.
  2. Download the credentials file and save as `credentials.json` in your project root.
  3. Add `http://localhost:8080/` as an authorized redirect URI.
  4. Add your Google account as a test user in the OAuth consent screen.
  5. Run the authentication script:
     ```bash
     python google_auth_setup.py
     ```
     - This will open a browser for you to log in and authorize access.
     - After successful login, a `token.json` file will be created.

- **Usage:**
  - The agent can schedule meetings directly in your Google Calendar when the call mentions scheduling a demo or follow-up.
  - The UI will show a clickable link to the created event.

### Web Search (SerpAPI)
- Add your SerpAPI key to `.env` as `SERPAPI_API_KEY`.
- The agent will use real-time web search to find competitor/product information when relevant.
- Results are shown as clickable links in the UI.
