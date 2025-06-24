# 🚀 Webex History Bot - GITHUB SYNC VERSION 2.0

✅ **UPDATED VIA GITHUB SYNC - If you see this, sync is working!**

A Flask-based Webex bot that generates and shares conversation history reports for recent room activity.

## Features
- 🔍 Fetches your recent Webex room activity (last 7 days)
- 📊 Generates interactive HTML reports with DataTables
- 🤖 Responds to bot commands in Webex rooms
- ☁️ Ready for Replit deployment

## Quick Start (Replit Deployment)

### 1. Fork/Import to Replit
1. Go to [Replit](https://replit.com)
2. Click "Create Repl" → "Import from GitHub"
3. Use your repository URL

### 2. Set Environment Variables
Create a `.env` file in the root directory with:
```bash
# Your personal Webex details
WEBEX_ACCESS_TOKEN=your_personal_access_token
WEBEX_ORG_ID=your_org_id

# Bot details (from Webex Developer Portal)
BOT_ACCESS_TOKEN=your_bot_access_token
BOT_NAME="Convo Lookback"
BOT_USERNAME="your-bot@webex.bot"
BOT_ID=your_bot_id
```

### 3. Get Your Tokens
- **Personal Token**: Go to [developer.webex.com](https://developer.webex.com) → Getting Started → Copy your personal access token
- **Bot Token**: Create a bot at [developer.webex.com](https://developer.webex.com) → My Webex Apps → Create New App → Bot

### 4. Run the Bot
- Click the "Run" button in Replit
- Your bot will start on the provided URL (e.g., `https://your-repl.username.repl.co`)

### 5. Set up Webex Webhook (Optional)
To receive messages from Webex:
1. Go to your bot settings in Webex Developer Portal
2. Add a webhook pointing to: `https://your-repl.username.repl.co/webhook`
3. Add the bot to Webex rooms where you want it to respond

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
pip install -r requirements.txt
python main.py
```

### Test Endpoints
- Health check: `GET http://localhost:5000/`
- Webhook: `POST http://localhost:5000/webhook`

## Usage

### Bot Commands
Send these messages to the bot:
- `summary` or `report` - Generate and receive a room activity report

### Direct Report Generation
```python
from report_generator import generate_report
file_path = generate_report()
```

## Configuration

- **Room limit**: Currently set to 50 rooms (adjust in `config.py`)
- **Time range**: Last 7 days (adjust in `report_generator.py`)
- **Ignored rooms**: Listed in `config.py`

## Files Structure
- `main.py` - Entry point and Flask app runner
- `bot.py` - Flask app with webhook handling
- `report_generator.py` - Main report generation logic
- `api.py` - Webex API interaction functions
- `html_report.py` - HTML report generation
- `config.py` - Configuration and environment variables
- `keep_alive.py` - Replit deployment helper

## Security Notes
- Never commit your `.env` file with real tokens
- Use Replit's Secrets feature for production deployments
- Tokens should have minimal required scopes
