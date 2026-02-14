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
3. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `SYNCRO_SUBDOMAIN`: Your Syncro MSP subdomain.
   - `SYNCRO_API_KEY`: Your Syncro MSP API key.
   - `SERP_API_KEY`: Optional, for external search.
4. Run the app: `python chatbot.py`
5. Open `index.html` in a browser to test the chat interface.

## API Endpoints
- `POST /chat`: Send a message and get a response. Body: `{"message": "your issue", "context": "previous context"}`

## Notes
- Expand the knowledge base to a database for production.
- Add user authentication and logging for security.
- Test integrations thoroughly.