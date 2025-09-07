from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Set your bot token in Render environment variables for security
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        # Echo bot reply
        reply = f"You said: {text}"
        payload = {
            "chat_id": chat_id,
            "text": reply
        }
        requests.post(TELEGRAM_API_URL, json=payload)

    return "ok", 200

if __name__ == "__main__":
    # Run Flask in Render free plan mode
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
