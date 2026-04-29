from flask import Flask, request
import requests

app = Flask(__name__)

WHATSAPP_TOKEN = "your_token_from_meta"
PHONE_NUMBER_ID = "your_phone_number_id"

@app.route("/webhook", methods=["GET"])
def verify():
    # Meta verification
    if request.args.get("hub.verify_token") == "mytoken123":
        return request.args.get("hub.challenge")
    return "Error", 403

@app.route("/webhook", methods=["POST"])
def receive():
    data = request.json
    message = data['entry'][0]['changes'][0]['value']['messages'][0]
    from_number = message['from']
    user_text = message['text']['body']

    # Simple AI reply (you can plug Claude API here)
    reply = f"SugarSaathi received: '{user_text}'. Your glucose coaching is being prepared!"

    # Send reply back via WhatsApp
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
        headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
        json={
            "messaging_product": "whatsapp",
            "to": from_number,
            "text": {"body": reply}
        }
    )
    return "OK", 200