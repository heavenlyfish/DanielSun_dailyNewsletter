# DanielSun_dailyNewsletter

DanielSun_dailyNewsletter

This project automates the daily download, backup, and Telegram notification of the Business Weekly Investor Daily PDF from the official website. It uses GitHub Actions to run daily at 9:00 PM Taiwan Time and includes MEGA cloud storage integration.

⸻

📌 Features
	•	✅ Scheduled Daily Download of the latest PDF
	•	✅ Taiwan Timezone Handling
	•	✅ Automatic Upload to MEGA via megacmd CLI
	•	✅ Telegram Notification & File Push
	•	✅ Automatic File Cleanup
	•	✅ Error Handling with Telegram Alerts

⸻

🛠️ Setup Instructions

1. Clone the Repository

git clone https://github.com/your-username/DanielSun_dailyNewsletter.git

2. Configure GitHub Secrets

Set the following secrets in your GitHub repository under Settings > Secrets > Actions:

Name	Description
MEGA_SESSION_ID	MEGA CLI session ID
TELEGRAM_BOT_TOKEN	Your Telegram bot token
TELEGRAM_CHAT_ID	Your chat ID for Telegram messaging

3. Schedule & Manual Trigger
	•	Daily at 13:00 UTC (21:00 GMT+8 Taipei)
	•	You can also trigger it manually via workflow_dispatch

⸻

📄 File Structure

DanielSun_dailyNewsletter/
├── .github/
│   └── workflows/
│       └── daily-upload.yml     # GitHub Actions workflow
├── download_bw_pdf.py          # Main automation script
├── .env.template               # Example .env file (for local test)
├── README.md                   # Project documentation


⸻

📜 GitHub Actions Workflow Summary (.github/workflows/daily-upload.yml)
	•	Installs Python dependencies
	•	Installs megacmd from official .deb
	•	Runs the Python script to download and send the file via Telegram
	•	Uploads the file to MEGA cloud storage

⸻

🧪 Local Testing

Create a .env file based on .env.template and run:

python3 download_bw_pdf.py

Ensure MEGA CLI is installed locally for full testing.

⸻

📬 Sample Telegram Output

InvestorDailyFile_20250611_投資家日報.pdf 已備份至 MEGA「InvestorDaily」
✅ InvestorDailyFile_20250611_投資家日報.pdf 已成功下載並備份至 MEGA & 傳送至 Telegram。


⸻

🤖 Credits & Contact

Created by Marvin Tu (2025)

Feel free to fork or contribute! If you’d like to expand this system to other newsletters or data sources, reach out!
