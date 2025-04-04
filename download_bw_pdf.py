#!/usr/bin/env python3
import asyncio
if not hasattr(asyncio, "coroutine"):
    asyncio.coroutine = lambda func: func

from dotenv import load_dotenv
load_dotenv()

import requests
from mega import Mega
import os
from datetime import datetime, timezone, timedelta

def send_telegram_message(message):
    """Send a text notification message via Telegram Bot."""
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_bot_token or not telegram_chat_id:
        print("Telegram credentials not found in environment variables.")
        return
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Telegram notification sent.")
    else:
        print("Failed to send Telegram notification. Response:", response.text)

def send_file_to_telegram(file_path, caption=""):
    """Send a file as a document to Telegram."""
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_bot_token or not telegram_chat_id:
        print("Telegram credentials not found in environment variables.")
        return
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendDocument"
    with open(file_path, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': telegram_chat_id, 'caption': caption}
        response = requests.post(url, data=data, files=files)
    if response.status_code == 200:
        print("File sent to Telegram successfully.")
    else:
        print("Failed to send file to Telegram. Response:", response.text)

def main():
    # Calculate current date in Taiwan time (UTC+8)
    tz = timezone(timedelta(hours=8))
    taiwan_date = datetime.now(tz)
    
    # Use the original file naming convention:
    # Part1 = YYYYMM, Part2 = YYYYMMDD.
    part1 = taiwan_date.strftime("%Y%m")
    part2 = taiwan_date.strftime("%Y%m%d")
    
    # Construct URL and file name using the original naming scheme.
    url = f"https://smart.businessweekly.com.tw/admin//MultUploadFile/InvestorDailyFile_{part1}{part2}_投資家日報.pdf"
    filename = f"InvestorDailyFile_{part1}{part2}_投資家日報.pdf"
    
    print("Downloading file from URL:", url)

    # Check if the file already exists locally
    if os.path.exists(filename):
        print(f"{filename} already exists. Skipping download.")
    else:
        # Download the file if it doesn't exist
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"{filename} downloaded.")
        else:
            error_message = "PDF not available or URL error."
            print(error_message)
            send_telegram_message(f"{error_message} for file: {filename}")
            exit()

    # Retrieve MEGA credentials from environment variables
    mega_email = os.environ.get("MEGA_EMAIL")
    mega_password = os.environ.get("MEGA_PASSWORD")
    if not mega_email or not mega_password:
        error_message = "MEGA credentials not found in environment variables."
        print(error_message)
        send_telegram_message(error_message)
        exit()

    # Login to MEGA
    mega = Mega()
    m = mega.login(mega_email, mega_password)

    # Check for the folder "InvestorDaily" in MEGA
    folder_name = "InvestorDaily"
    folder = m.find(folder_name)

    if folder:
        folder_node = folder[0]
        print(f"Folder '{folder_name}' found.")
    else:
        folder_node = m.create_folder(folder_name)
        print(f"Folder '{folder_name}' created.")

    # Upload the file to the specified folder and capture the returned node
    uploaded_node = m.upload(filename, folder_node)
    print(f"{filename} uploaded to MEGA in folder '{folder_name}'.")

    # (Skip renaming step)

    # Send a copy of the file to Telegram as a document.
    send_file_to_telegram(filename, caption=f"File {filename} has been uploaded to MEGA in folder '{folder_name}'.")

    # Optionally delete the local file after sending to Telegram and uploading to MEGA
    os.remove(filename)
    print("Local file deleted.")

    # Send a final Telegram notification
    send_telegram_message(f"File {filename} successfully processed and sent via Telegram.")

if __name__ == '__main__':
    main()