import yfinance as yf
import requests
import os

# --- 1. รายชื่อหุ้นในพอร์ตของคุณ (แก้ไขชื่อหุ้นและทุนตรงนี้) ---
MY_PORTFOLIO = {
    "SIRI.BK": 1.40,
    "BTS.BK": 9.02,
    "TWPC.BK": 11.42,
    "GLD.BK": 6.66,
}

# --- 2. ดึงค่าจาก GitHub Secrets ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def check_stocks():
    message = "🔔 รายงานพอร์ตหุ้นวันนี้\n\n"
    for symbol, cost in MY_PORTFOLIO.items():
        try:
            stock = yf.Ticker(symbol)
            # ดึงราคาล่าสุด
            current = stock.history(period="1d")['Close'].iloc[-1]
            diff = ((current - cost) / cost) * 100
            status = "🟢" if diff >= 0 else "🔴"
            
            message += f"{status} {symbol}\n"
            message += f"ราคา: {current:.2f} (ทุน: {cost:.2f})\n"
            message += f"กำไร/ขาดทุน: {diff:+.2f}%\n\n"
        except:
            message += f"❌ ดึงข้อมูล {symbol} ไม่ได้\n"
    return message

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        report = check_stocks()
        send_telegram(report)
    else:
        print("Error: Please set Secrets in GitHub Settings")
