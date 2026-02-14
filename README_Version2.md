# Tier 1 Support Chatbot

This is a prototype for a tier 1 support chatbot designed to reduce frivolous tickets for tier 2 technicians. It uses OpenAI's GPT-3.5-turbo for AI inference, guides users through non-technical remediations (e.g., password resets, email issues, printer problems), and integrates with Syncro MSP for ticket escalation.

## Features
- AI-powered conversation with step-by-step guidance.
- Knowledge base for common issues.
- External search for unknown queries.
- Escalation to tier 2 via Syncro MSP API.
- Fully remote focus (no on-site visits; shipping options for hardware).

## Setup
1. Clone this repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API keys:
   - Copy `.env.example` to `.env` and fill in your API keys
   - OR set environment variables manually (see [API_KEYS.md](API_KEYS.md) for details):
     - `OPENAI_API_KEY`: Your OpenAI API key (required)
     - `SYNCRO_SUBDOMAIN`: Your Syncro MSP subdomain (required)
     - `SYNCRO_API_KEY`: Your Syncro MSP API key (required)
     - `SERP_API_KEY`: Optional, for external search
   - **See [API_KEYS.md](API_KEYS.md) for detailed instructions on obtaining each API key**
4. Run the app: `python chatbot.py`
5. Open `index.html` in a browser to test the chat interface.

## API Endpoints
- `POST /chat`: Send a message and get a response. Body: `{"message": "your issue", "context": "previous context"}`

## API Keys Required

This application requires several API keys to function. See [API_KEYS.md](API_KEYS.md) for:
- Complete list of required and optional API keys
- Step-by-step instructions for obtaining each key
- Security best practices
- Troubleshooting common issues

Quick reference:
- **OpenAI API** (required): For AI-powered responses
- **Syncro MSP API** (required): For ticket escalation
- **SerpAPI** (optional): For external web search

## Notes
- Expand the knowledge base to a database for production.
- Add user authentication and logging for security.
- Test integrations thoroughly.