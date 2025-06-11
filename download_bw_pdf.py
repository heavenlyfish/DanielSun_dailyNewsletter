#!/usr/bin/env python3
import asyncio
if not hasattr(asyncio, "coroutine"):
    asyncio.coroutine = lambda func: func

from dotenv import load_dotenv
load_dotenv()

import requests
import os
from datetime import datetime, timezone, timedelta

def send_telegram_message(message):
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_bot_token or not telegram_chat_id:
        print("Telegram credentials not found in environment variables.")
        return
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    try:
        response = requests.post(url, data=payload, timeout=15)
        if response.status_code == 200:
            print("Telegram notification sent.")
        else:
            print("Failed to send Telegram message. Code:", response.status_code, "Response:", response.text)
    except Exception as e:
        print("Error sending Telegram message:", e)

def send_file_to_telegram(file_path, caption=""):
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_bot_token or not telegram_chat_id:
        print("Telegram credentials not found in environment variables.")
        return
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': telegram_chat_id, 'caption': caption}
            response = requests.post(url, data=data, files=files, timeout=30)
        if response.status_code == 200:
            print("File sent to Telegram successfully.")
        else:
            print("Failed to send file to Telegram. Code:", response.status_code, "Response:", response.text)
    except Exception as e:
        print("Error sending file to Telegram:", e)

def main():
    tz = timezone(timedelta(hours=8))
    taiwan_date = datetime.now(tz)

    part1 = taiwan_date.strftime("%Y%m")
    part2 = taiwan_date.strftime("%Y%m%d")
    url = f"https://smart.businessweekly.com.tw/admin//MultUploadFile/InvestorDailyFile_{part1}{part2}_投資家日報.pdf"
    filename = f"InvestorDailyFile_{part1}{part2}_投資家日報.pdf"

    print("Downloading file from URL:", url)

    if os.path.exists(filename):
        print(f"{filename} already exists. Skipping download.")
    else:
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"{filename} downloaded.")
            else:
                msg = f"❌ PDF not found or failed to download: {response.status_code}"
                print(msg)
                send_telegram_message(msg)
                exit(1)
        except Exception as e:
            print("Download failed:", e)
            send_telegram_message(f"❌ PDF download error: {e}")
            exit(1)

    send_file_to_telegram(filename, caption=f"{filename} 已備份至 MEGA「InvestorDaily」")
    os.remove(filename)
    print("✅ Local file deleted.")

    send_telegram_message(f"✅ {filename} 已成功下載並備份至 MEGA & 傳送至 Telegram。")

if __name__ == '__main__':
    main()
