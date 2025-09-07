from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Bot token from environment variables (set in Render)
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/')
def home():
    return "Bot is running!"

# Debug route for browser GET requests (optional)
@app.route(f'/webhook/{TOKEN}', methods=['GET'])
def webhook_test():
    return "Webhook is live! ✅", 200

# Telegram webhook POST route
@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming update:", data)  # Debug: check Telegram updates

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Handle /start command
        if text == "/start":
            reply = "Welcome to my bot! 😎\nYou can type anything and I'll echo it back."
        else:
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
