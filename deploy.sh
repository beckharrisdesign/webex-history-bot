#!/bin/bash

# Webex History Bot - Quick Deploy Script
echo "🚀 Deploying Webex History Bot..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📋 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial Webex History Bot commit"
fi

# Check for changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing changes..."
    git add .
    git commit -m "Updated bot code - $(date)"
else
    echo "✅ No changes to commit"
fi

# Push to GitHub (you'll need to set up remote first)
echo "📤 Pushing to GitHub..."
if git remote | grep -q origin; then
    git push origin main
    echo "✅ Pushed to GitHub successfully!"
    echo "🔗 Now go to Replit and pull the latest changes"
else
    echo "❌ No origin remote found. Please set up GitHub first:"
    echo "   1. Create a repo on GitHub"
    echo "   2. Run: git remote add origin https://github.com/yourusername/webex-history-bot.git"
    echo "   3. Run: git push -u origin main"
fi

echo "🎉 Deployment script complete!"
