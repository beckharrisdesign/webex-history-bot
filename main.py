from bot import app
from keep_alive import keep_alive
import os

if __name__ == "__main__":
    print("🤖 Starting Webex History Bot...")
    print("🔗 GITHUB SYNC VERSION 2.0")
    print("📝 Repository: https://github.com/beckharrisdesign/webex-history-bot")
    print("=" * 60)
    
    # Start keep-alive thread for Replit
    keep_alive()
    
    port = int(os.environ.get("PORT", 3000))
    
    # More verbose logging for debugging
    print(f"🚀 Bot starting on port {port}")
    print(f"📊 Bot name: {os.getenv('BOT_NAME', 'Webex History Bot')}")
    print(f"🔗 Health check: http://localhost:{port}/")
    print(f"🪝 Webhook: http://localhost:{port}/webhook")
    print("=" * 60)
    print("✅ READY TO RECEIVE WEBHOOKS!")
    
    app.run(host="0.0.0.0", port=port, debug=False)
