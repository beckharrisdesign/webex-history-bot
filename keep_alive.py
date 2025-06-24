import threading
import time
import requests

def keep_alive():
    """
    Simple keep-alive function for Replit deployment.
    Prevents the bot from going to sleep by making periodic self-requests.
    """
    def run():
        while True:
            try:
                # Make a simple request to keep the server alive
                # This assumes your bot is running on the default port
                requests.get("http://localhost:5000", timeout=5)
                print("[INFO] Keep-alive ping sent")
            except Exception as e:
                print(f"[WARNING] Keep-alive ping failed: {e}")
            
            # Wait 5 minutes before next ping
            time.sleep(300)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print("[INFO] Keep-alive thread started")