import os
import requests
from flask import Flask

app = Flask(__name__)

def send_telegram_message(text: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return "Telegram env not set"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(url, json=payload, timeout=10)
    return r.text


@app.route("/")
def home():
    return "MyTradingBot is running on Render"


@app.route("/test-telegram")
def test_telegram():
    result = send_telegram_message("✅ Telegram connected from Render!")
    return result
    
