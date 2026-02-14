import os
from flask import Flask, request, jsonify
import openai
import requests  # For external API calls, e.g., search or Syncro MSP ticketing

app = Flask(__name__)

# Set up OpenAI API (replace with your key)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Syncro MSP API configuration (replace with your subdomain and API key)
SYNCRO_SUBDOMAIN = os.getenv('SYNCRO_SUBDOMAIN')  # e.g., 'yourcompany'
SYNCRO_API_KEY = os.getenv('SYNCRO_API_KEY')

# Expanded knowledge base (expand to a database or JSON file for scalability)
KNOWLEDGE_BASE = {
    "password reset": {
        "response": "To reset your password: 1. Visit the self-service portal at https://reset.company.com. 2. Click 'Forgot Password' and enter your username. 3. Follow the email instructions. If this doesn't work, provide more details.",
        "steps": ["Visit portal", "Enter username", "Check email"]
    },
    "email issue": {
        "response": "For email problems: 1. Check your spam/junk folder. 2. Verify IMAP/POP settings in your client. 3. Try logging out and back in. Describe your issue for more help.",
        "steps": ["Check spam", "Verify settings", "Logout/login"]
    },
    "printer issue": {
        "response": "Printer troubleshooting: 1. Restart the printer. 2. Check network connection (ping the IP). 3. Clear print queue. If remote, request shipping via our portal at https://shipping.company.com.",
        "steps": ["Restart device", "Check network", "Clear queue"]
    }
}

def get_ai_response(user_message, context=""):
    # Enhanced prompt for AI inference with context
    prompt = f"""
    You are a tier 1 support chatbot for a fully remote company. Guide users through remediation for non-technical issues like password resets, email, or printers.
    - Be helpful, step-by-step, and confirm actions.
    - If the issue is complex or unresolved after guidance, suggest escalation to tier 2.
    - Do not suggest on-site visits; focus on remote solutions like shipping if hardware-related.
    - Pull from knowledge base if possible, but use logic for new queries.
    Context from previous interaction: {context}
    User says: {user_message}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message['content']

def search_external_info(query):
    # Example: Use SerpAPI for web search (sign up for API key)
    api_key = os.getenv('SERP_API_KEY')
    url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('organic_results', [])
        return results[0]['snippet'] if results else "No external info found."
    return "Unable to search."

def create_syncro_ticket(subject, description):
    # Syncro MSP API integration for ticket creation
    url = f"https://{SYNCRO_SUBDOMAIN}.syncromsp.com/api/v1/tickets"
    headers = {
        'Authorization': f'Bearer {SYNCRO_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "subject": subject,
        "description": description,
        "status": "New",  # Adjust based on Syncro's ticket statuses
        "priority": "Normal"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        ticket = response.json()
        return f"Ticket created successfully. Ticket ID: {ticket.get('id')}"
    else:
        return f"Failed to create ticket: {response.text}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()
    context = data.get('context', '')  # Optional: Pass previous context for multi-turn conversations
    
    response = ""
    
    # Check knowledge base first for exact matches
    matched_key = next((key for key in KNOWLEDGE_BASE if key in user_message), None)
    if matched_key:
        kb_item = KNOWLEDGE_BASE[matched_key]
        response = kb_item["response"]
        # Simulate step-by-step guidance
        if "yes" in user_message or "next" in user_message:
            steps = kb_item["steps"]
            current_step = data.get('step', 0)
            if current_step < len(steps):
                response = f"Step {current_step + 1}: {steps[current_step]}"
            else:
                response = "All steps completed. Did this resolve your issue? If not, say 'escalate'."
    else:
        # Use AI for inference on unknown queries
        response = get_ai_response(user_message, context)
    
    # Handle escalation
    if "escalate" in user_message.lower() or ("tier 2" in response.lower() and "escalate" in user_message.lower()):
        ticket_result = create_syncro_ticket("Tier 1 Escalation", f"User issue: {user_message}. Bot response: {response}")
        response += f" {ticket_result}"
    
    # Pull external info if needed
    if "unknown" in response.lower() or "search" in user_message.lower():
        external_info = search_external_info(user_message)
        response += f" Additional info: {external_info}"
    
    # Return response with context for next turn
    return jsonify({
        "response": response,
        "context": context + f" User: {user_message}. Bot: {response}."
    })

if __name__ == '__main__':
    app.run(debug=True)