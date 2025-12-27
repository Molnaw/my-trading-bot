from flask import Flask, request, jsonify
import os
from okx.api_v5 import Trade as Trade
from okx.api_v5 import MarketData as MarketData

app = Flask(__name__)

# ดึงค่า API OKX จากที่ตั้งไว้ใน Render
API_KEY = os.environ.get("OKX_API_KEY")
API_SECRET = os.environ.get("OKX_API_SECRET")
API_PASSPHRASE = os.environ.get("OKX_API_PASSPHRASE")

# ตั้งค่าเชื่อมต่อ OKX (ใช้ '0' สำหรับบัญชีจริง, '1' สำหรับบัญชี Demo)
flag = '0' 
trade_api = Trade.TradeAPI(API_KEY, API_SECRET, API_PASSPHRASE, False, flag)

@app.route("/", methods=["GET"])
def home():
    return "<h1>OKX Trading Bot is Running 24/7</h1>", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    # รับค่าจาก Signal (เช่น {"action": "buy", "symbol": "BTC-USDT", "size": "0.001"})
    side = data.get("action")  # 'buy' หรือ 'sell'
    symbol = data.get("symbol") # เช่น 'BTC-USDT'
    size = data.get("size")     # จำนวนที่ต้องการเทรด

    try:
        # ส่งคำสั่ง Market Order ไปยัง OKX
        result = trade_api.place_order(
            instId=symbol,
            tdMode='cash',
            side=side,
            ordType='market',
            sz=size
        )
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
นาย
