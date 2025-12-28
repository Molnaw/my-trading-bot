from flask import Flask, request, jsonify
import os
import okx.Trade as Trade

app = Flask(__name__)

# ดึงค่า API จาก Environment Variables ของ Render
API_KEY = os.environ.get("OKX_API_KEY")
API_SECRET = os.environ.get("OKX_API_SECRET")
API_PASSPHRASE = os.environ.get("OKX_API_PASSPHRASE")

# เชื่อมต่อ OKX (flag '0' คือบัญชีจริง, '1' คือบัญชี Demo)
# ตรวจสอบให้แน่ใจว่าได้ตั้งค่า Environment Variables ในหน้า Dashboard ของ Render แล้ว
trade_api = Trade.TradeAPI(API_KEY, API_SECRET, API_PASSPHRASE, False, flag='0')

@app.route("/", methods=["GET"])
def home():
    return "<h1>OKX Trading Bot is Live 24/7</h1>", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        # รับค่าจาก Webhook เช่น {"action": "buy", "symbol": "BTC-USDT", "size": "0.1"}
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
