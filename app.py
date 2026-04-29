from flask import Flask, request
import requests
import os

app = Flask(__name__)

WHATSAPP_TOKEN = "EAANd56KobBwBRbpt3cJK9yotQdTiHZCPnZBtKKtVKi9UjC0LIJwZBCpxlK7mYXY6AT1nMgWKpZBNtCbMYTW41ZCbc7yuSBHgYGKZA060ivlieTg6qrJNgj6SvUI8DzetIxtYgnBZAuPqNH4ARMERo26HPK2FO3ZB6ysTIKZAiDd1IJd1tfSpp1UBabKfG1MNbUFSGn4nzYv6raHbPAxv1rGeyyv4aIz2fUhlIF6Rbg8RrwIq4okB61K1cgoMw0kgdvD8w6VqEbDZBrzWAdnqbsZCdZBPKDZCg"
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