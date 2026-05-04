from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# 🔐 IMPORTANT: Replace with your NEW token (regenerate if exposed)
WHATSAPP_TOKEN = "1159201907265696"
PHONE_NUMBER_ID = "EAANd56KobBwBRf4R4ZBw9juInYzP0HWnpQ26Bv7VxhskWav2XIqE9NEZBltVfxqZBZBVBWfe7E4dGeDTUzJPxqxBORIfSiYtwft4TcGZBBlEOQFAblv6ZCd1OfDaWmYZAuuoSWQFbN2MBRe7rqCwVH49833trvmmTZCDk7gVwxwYeyHcXKk15N54ojZCSSZCKKCIo64DZCsRhb3oCG3JjhdrHsO7mU4imFTx2posD2jiZAc7KDR7CWVlR3RrYxS7PXZA641q9IqhHTE6jHaQFxSZBK1YQDgna1mAFfbfDZBzXlWhgZDZD"

VERIFY_TOKEN = "mytoken123"

# 📁 File to store processed message IDs
IDS_FILE = "ids.json"


# ✅ Load processed IDs from file
def load_ids():
    try:
        with open(IDS_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


# ✅ Save processed IDs to file
def save_ids(ids):
    with open(IDS_FILE, "w") as f:
        json.dump(list(ids), f)


processed_ids = load_ids()


# 🔹 Webhook verification (GET)
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Error", 403


# 🔹 Webhook receiver (POST)
@app.route("/webhook", methods=["POST"])
def receive():
    data = request.json

    # ✅ Always respond fast (VERY IMPORTANT)
    process_message(data)
    return "OK", 200


# 🔹 Main logic
def process_message(data):
    try:
        value = data['entry'][0]['changes'][0]['value']

        # ❌ Ignore non-message events
        if 'messages' not in value:
            return

        message = value['messages'][0]

        # ❌ Only handle text messages
        if message.get("type") != "text":
            return

        message_id = message['id']
        from_number = message['from']
        user_text = message['text']['body']

        print("Incoming message:", user_text)
        print("Message ID:", message_id)

        # ✅ Deduplication check
        if message_id in processed_ids:
            print("Duplicate message ignored")
            return

        processed_ids.add(message_id)
        save_ids(processed_ids)

        # 🤖 Your reply (can replace with AI later)
        reply = f"SugarSaathi received: '{user_text}'. Your glucose coaching is being prepared!"

        # 📤 Send reply via WhatsApp API
        response = requests.post(
            f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
            headers={
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "messaging_product": "whatsapp",
                "to": from_number,
                "text": {"body": reply}
            }
        )

        print("Sent reply:", response.status_code, response.text)

    except Exception as e:
        print("Error processing message:", e)


# 🔹 Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))