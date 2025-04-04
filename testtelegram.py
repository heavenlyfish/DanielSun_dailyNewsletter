import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(message):
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_bot_token or not telegram_chat_id:
        print("Telegram credentials not found in environment variables.")
        return
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, data=payload)
    print("Response status code:", response.status_code)
    print("Response text:", response.text)

send_telegram_message("Test message from your bot!")