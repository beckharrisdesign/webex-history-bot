# 🚀 Webex History Bot - GITHUB SYNC VERSION 2.0

✅ **UPDATED VIA GITHUB SYNC - If you see this, sync is working!**

A Flask-based Webex bot that generates and shares conversation history reports for recent room activity.

## 📋 Recent Changes & Status

### Current Status: ✅ FULLY FUNCTIONAL (June 24, 2025)
- ✅ Local development server working on port 3000
- ✅ Public tunnel via Cloudflare working  
- ✅ Webhook communication verified and FIXED
- ✅ Message text parsing FIXED (major bug resolved)
- ✅ Report generation and file sending working
- ✅ Command detection ("summary"/"report") working perfectly
- ✅ Code backed up to GitHub (beckharrisdesign/webex-history-bot)

### Latest Updates (v2.1 - MAJOR FIX)
- **June 24, 2025**: 🎯 **CRITICAL BUG FIXED** - Message text parsing now working!
- **Added**: `get_message_text()` function to fetch actual message content via API
- **Fixed**: Webhook text parsing (webhooks don't include text directly)
- **Enhanced**: Comprehensive debugging and error handling
- **Verified**: Commands "summary" and "report" now work perfectly
- **2024**: Migrated from Replit to local development with public tunnel

### Ready for Development 🛠️
The bot is fully functional and ready for further development. See the "Returning Developer Guide" below for restart instructions.

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
- Health check: `GET http://localhost:3000/`
- Webhook: `POST http://localhost:3000/webhook`

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

## Returning Developer Guide 🔄

**For restarting development after closing your computer or returning to the project:**

### Step 1: Start the Local Server
```bash
cd /path/to/webex-history-bot
python main.py
```
✅ **Expected**: Server starts on `http://localhost:3000` with startup banner

### Step 2: Set Up Public Tunnel
In a **new terminal** (keep the server running):
```bash
# Install cloudflared if not already installed
brew install cloudflared

# Create tunnel to your local server
cloudflared tunnel --url http://localhost:3000
```
✅ **Expected**: You'll get a public URL like `https://xyz-abc-123.trycloudflare.com`

**📋 Copy this URL - you'll need it for the webhook!**

### Step 3: Update Webex Webhook
1. Go to [Webex Developer Portal](https://developer.webex.com)
2. Navigate to "My Webex Apps" → Your Bot
3. Update the webhook URL to: `https://your-tunnel-url.trycloudflare.com/webhook`
4. Save changes

### Step 4: Test the Bot
1. Open Webex and find your bot in contacts
2. Send a direct message: `summary` or `report`
3. Check terminal logs for webhook activity
4. Bot should respond with a conversation history report

### Quick Status Check
- ✅ **Server**: Check `http://localhost:3000` shows "Webex History Bot is running!"
- ✅ **Tunnel**: Check your tunnel URL is accessible publicly
- ✅ **Webhook**: Verify webhook URL in Webex Developer Portal matches your tunnel
- ✅ **Bot**: Send test message and check terminal for webhook logs

### Troubleshooting
- **No webhook calls**: Double-check webhook URL matches your current tunnel
- **Bot not responding**: Check `.env` file has correct BOT_ACCESS_TOKEN
- **Tunnel expired**: Restart cloudflared (tunnels expire after ~4 hours)
- **API errors**: Verify your personal WEBEX_ACCESS_TOKEN is valid

### Daily Workflow Summary
1. `python main.py` (start server)
2. `cloudflared tunnel --url http://localhost:3000` (new terminal)
3. Update webhook URL with new tunnel URL
4. Test bot with a message
5. Code, test, commit to GitHub

## Files Structure
- `main.py` - Entry point and Flask app runner
- `bot.py` - Flask app with webhook handling
- `report_generator.py` - Main report generation logic
- `api.py` - Webex API interaction functions
- `html_report.py` - HTML report generation
- `config.py` - Configuration and environment variables
- `keep_alive.py` - Replit deployment helper
- `debug_webhook.py` - Webhook debugging utility
- `TUNNEL_STATUS.md` - Tunnel documentation
- `GITHUB_SYNC_TEST.md` - GitHub sync verification

## Security Notes
- Never commit your `.env` file with real tokens
- Use Replit's Secrets feature for production deployments
- Tokens should have minimal required scopes
