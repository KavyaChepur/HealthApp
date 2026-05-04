from flask import Flask, request
import requests
import os

app = Flask(__name__)

WHATSAPP_TOKEN = "EAANd56KobBwBRfhNZBbQEhjBJ8ZANd3BQynFf3g4NYdQv4rvCEYQbgNEkuU4AifZAmRe0j2Gkgy6ZCNgrsZAaFW6YJmdZAij2NZA9K2GkLU7v5XZBfohWqGGJ6udwINBqPjZBMBMJU30kOuOWLz51SpjEPrXZA7mALnS0vPlohI4SkULhcmfmUCylZB9yjSqTzGZBb5eShJsKXZAcYOnvXYZCQft2xLy9kkpmz7yC2ILKD4xGqnX52MiZABXqJ1WS7Q0OZA6CPGZCChPE94xi4wSWIBpM5eOJ5EqFq7aYAVWs3Q9chwUZD"
PHONE_NUMBER_ID = "1159201907265696"

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
    if message.get("type") != "text":
        return "OK", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))