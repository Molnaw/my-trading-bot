
from flask import Flask, request, jsonify
import os
import requests
import pandas as pd
import pandas_ta as ta
import okx.MarketData as MarketData
import okx.Trade as Trade
import time
from threading import Thread

app = Flask(__name__)

# ตั้งค่า API
API_KEY = os.environ.get("OKX_API_KEY")
API_SECRET = os.environ.get("OKX_API_SECRET")
API_PASSPHRASE = os.environ.get("OKX_API_PASSPHRASE")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# เชื่อมต่อ API
market_api = MarketData.MarketAPI(flag='0')
trade_api = Trade.TradeAPI(API_KEY, API_SECRET, API_PASSPHRASE, False, flag='0')

def send_telegram(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})

def bot_strategy():
    """ฟังก์ชันคำนวณกลยุทธ์ RSI และเทรดอัตโนมัติ"""
    symbol = "BTC-USDT"
    size = "0.001" # ปรับจำนวนตามต้องการ
    
    while True:
        try:
            # 1. ดึงข้อมูลราคาล่าสุด
            candles = market_api.get_candlesticks(instId=symbol, bar='1m', limit=50)
            df = pd.DataFrame(candles['data'], columns=['ts', 'o', 'h', 'l', 'c', 'v', 'vol', 'volC', 'confirm'])
            df['c'] = df['c'].astype(float)
            
            # 2. คำนวณ RSI
            df['rsi'] = ta.rsi(df['c'], length=14)
            current_rsi = df['rsi'].iloc[0]
            
            # 3. เงื่อนไขการเทรด
            if current_rsi < 30: # จุดซื้อ (Oversold)
                trade_api.place_order(instId=symbol, tdMode='cash', side='buy', ordType='market', sz=size)
                send_telegram(f"🛒 *BUY {symbol}*\nRSI: {current_rsi:.2f}")
            
            elif current_rsi > 70: # จุดขาย (Overbought)
                trade_api.place_order(instId=symbol, tdMode='cash', side='sell', ordType='market', sz=size)
                send_telegram(f"💰 *SELL {symbol}*\nRSI: {current_rsi:.2f}")

        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(60) # พัก 1 นาทีแล้วเช็คใหม่

# รันกลยุทธ์ใน Background
Thread(target=bot_strategy).start()

@app.route("/")
def home():
    return "<h1>OKX Auto-Trading Bot is Running...</h1>", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
