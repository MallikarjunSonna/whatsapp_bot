import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
from transformers import pipeline

# Load environment variables from .env
load_dotenv()

# Load chatbot model
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-small")

def generate_response(message):
    response = chatbot(message, max_length=100, do_sample=True)
    return response[0]["generated_text"]

app = Flask(__name__)

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is running!"

# ✅ Add this Webhook route for Meta verification
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token_sent = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token_sent == VERIFY_TOKEN:
            return challenge  # Meta expects this response
        else:
            return "Invalid verification token", 403

    elif request.method == "POST":
        data = request.json
        print("Received webhook data:", data)
        return jsonify({"status": "success"}), 200

@app.route("/send-message", methods=["POST"])
def send_whatsapp_message():
    data = request.json
    recipient = data.get("recipient")
    message = data.get("message")

    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

