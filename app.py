from flask import Flask, request, jsonify
import os
from okx.api_v5 import Trade as Trade

app = Flask(__name__)

# ดึงค่า API OKX ที่คุณใส่ไว้ใน Environment Variables ของ Render
API_KEY = os.environ.get("OKX_API_KEY")
API_SECRET = os.environ.get("OKX_API_SECRET")
API_PASSPHRASE = os.environ.get("OKX_API_PASSPHRASE")

# เชื่อมต่อ OKX (flag '0' คือบัญชีจริง)
# ตรวจสอบให้แน่ใจว่าได้ตั้งค่าเหล่านี้ในหน้า Environment ของ Render แล้ว
trade_api = Trade.TradeAPI(API_KEY, API_SECRET, API_PASSPHRASE, False, '0')

@app.route("/", methods=["GET"])
def home():
    return "<h1>OKX Trading Bot is Live 24/7</h1>", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        # รับค่าจาก Google Colab เช่น {"action": "buy", "symbol": "BTC-USDT", "size": "0.001"}
        result = trade_api.place_order(
            instId=data.get("symbol"),
            tdMode='cash',
            side=data.get("action"),
            ordType='market',
            sz=data.get("size")
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
