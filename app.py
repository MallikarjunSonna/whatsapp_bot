import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
WHATSAPP_CUSTOMER_KEY = os.getenv("WHATSAPP_CUSTOMER_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is running!"

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
