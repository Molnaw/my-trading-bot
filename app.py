from flask import Flask, request, jsonify
import os
import requests
import binance # อย่าลืมเพิ่ม python-binance ใน requirements.txt ทีหลังนะครับ

app = Flask(__name__)

# ดึงค่าจาก Environment Variables ที่คุณตั้งไว้ใน Render
API_KEY = os.environ.get("BINANCE_API_KEY")
API_SECRET = os.environ.get("BINANCE_API_SECRET")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Trading Bot is Live 24/7</h1>"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    # สมมติว่าสัญญาณส่งมาเป็น {"action": "buy", "symbol": "BTCUSDT"}
    action = data.get("action")
    symbol = data.get("symbol", "BTCUSDT")
    
    message = f"📢 ได้รับสัญญาณ: {action} {symbol}"
    send_telegram(message)
    
    # ตรงนี้คือส่วนที่จะใส่คำสั่งซื้อขายจริง (Execute Trade)
    # ผมจะรอคุณยืนยันชื่อ Exchange อีกครั้งเพื่อเขียนคำสั่งที่ถูกต้องให้ครับ
    
    return jsonify({"status": "success", "message": "Signal received"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
