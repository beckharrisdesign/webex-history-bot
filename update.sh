#!/bin/bash

# Quick update script for Webex History Bot
echo "🔄 Updating Webex History Bot..."

# Add and commit changes
git add .
git commit -m "Bot updates - $(date)"

# Push to GitHub
git push origin main

echo "✅ Updates pushed to GitHub!"
echo "🔗 Repository: https://github.com/beckharrisdesign/webex-history-bot"
echo "📝 Now go to Replit and pull the latest changes"
