# File: app.py
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from agent import create_agent

# --- Installation Required: pip install Flask twilio ---

app = Flask(__name__)

# Create the agent only once when the app starts
print("Initializing Krishi-Mitra Agent...")
krishi_agent = create_agent()
print("Agent Initialized.")

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Receives an SMS, gets an answer from the AI agent, and replies."""
    # Get the incoming message from the POST request
    incoming_msg = request.values.get('Body', '').strip()
    print(f"Received message: {incoming_msg}")

    # Create a default response
    response_text = "Sorry, I couldn't process your request right now. Please try again later."

    if incoming_msg:
        # Let the agent handle the query
        agent_response = krishi_agent.invoke({"input": incoming_msg})
        response_text = agent_response['output']

    # Create a Twilio response object to send the reply
    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)

if __name__ == "__main__":
    # To make this publicly accessible for Twilio, use a tool like ngrok
    # In your terminal, run: ngrok http 5000
    app.run(port=5000, debug=True)