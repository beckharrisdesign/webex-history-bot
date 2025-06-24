from flask import Flask, request, jsonify
import os
import requests

# Handle both relative and absolute imports
try:
    from .report_generator import generate_report
except ImportError:
    from report_generator import generate_report

app = Flask(__name__)

WEBEX_BOT_TOKEN = os.getenv('BOT_ACCESS_TOKEN', '')
WEBEX_API_URL = 'https://webexapis.com/v1/messages'

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': '🚀 Bot is RUNNING with GitHub sync!', 
        'name': os.getenv('BOT_NAME', 'Webex History Bot'),
        'version': '2.0.0-GITHUB-SYNC',
        'timestamp': '2025-06-24 UPDATED',
        'github_repo': 'https://github.com/beckharrisdesign/webex-history-bot',
        'message': '✅ If you see this, GitHub sync is working!'
    }), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print(f"[DEBUG] Full webhook data: {data}")  # Debug line
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
            
        # Ignore messages sent by the bot itself
        person_email = data.get('data', {}).get('personEmail', '')
        bot_email = os.getenv('BOT_USERNAME', '')
        print(f"[DEBUG] Person email: {person_email}, Bot email: {bot_email}")  # Debug line
        
        if person_email == bot_email:
            print("[DEBUG] Ignoring bot's own message")  # Debug line
            return jsonify({'status': 'ignored'}), 200
            
        # Get message details
        message_id = data.get('data', {}).get('id', '')
        room_id = data.get('data', {}).get('roomId', '')
        
        print(f"[DEBUG] Message ID: {message_id}")  # Debug line
        print(f"[DEBUG] Room ID: {room_id}")  # Debug line
        
        # Fetch the actual message content using the message ID
        text = ''
        if message_id:
            text = get_message_text(message_id)
            print(f"[DEBUG] Fetched message text: '{text}'")  # Debug line
        else:
            print("[DEBUG] No message ID found in webhook data")  # Debug line
        
        if not room_id:
            print("[ERROR] No room ID provided")  # Debug line
            return jsonify({'status': 'error', 'message': 'No room ID provided'}), 400
            
        # Check if this is a command
        text_lower = text.lower() if text else ''
        print(f"[DEBUG] Checking for commands in: '{text_lower}'")  # Debug line
        print(f"[DEBUG] 'summary' in text: {'summary' in text_lower}")  # Debug line
        print(f"[DEBUG] 'report' in text: {'report' in text_lower}")  # Debug line
            
        if 'summary' in text_lower or 'report' in text_lower:
            print("[DEBUG] Summary/report command detected!")  # Debug line
            try:
                send_message(room_id, '🔄 Generating your Webex activity report... This may take a moment.')
                print("[DEBUG] Starting report generation...")  # Debug line
                file_path = generate_report()
                print(f"[DEBUG] Report generated at: {file_path}")  # Debug line
                send_message(room_id, '✅ Webex summary report generated! See attached HTML file.')
                send_file(room_id, file_path)
                print("[DEBUG] Report sent successfully!")  # Debug line
            except Exception as e:
                print(f"[ERROR] Failed to generate report: {e}")
                import traceback
                traceback.print_exc()  # Print full stack trace
                send_message(room_id, f'❌ Sorry, I encountered an error generating the report: {str(e)}')
        else:
            print(f"[DEBUG] No summary/report command found in: '{text_lower}'")  # Debug line
            send_message(room_id, '👋 Hi! Send "summary" or "report" to get your Webex activity summary.')
            
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

def send_message(room_id, text):
    headers = {
        'Authorization': f'Bearer {WEBEX_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'roomId': room_id,
        'text': text
    }
    requests.post(WEBEX_API_URL, headers=headers, json=payload)

def send_file(room_id, file_path):
    headers = {
        'Authorization': f'Bearer {WEBEX_BOT_TOKEN}'
    }
    files = {
        'files': (os.path.basename(file_path), open(file_path, 'rb'), 'text/html')
    }
    data = {
        'roomId': room_id,
        'text': 'Download your Webex summary report:'
    }
    response = requests.post(WEBEX_API_URL, headers=headers, data=data, files=files)
    if response.status_code != 200:
        print(f"[ERROR] Failed to send file: {response.status_code}, {response.text}")

def get_message_text(message_id):
    """Fetch the actual text content of a message using its ID"""
    headers = {
        'Authorization': f'Bearer {WEBEX_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    message_url = f"https://webexapis.com/v1/messages/{message_id}"
    response = requests.get(message_url, headers=headers)
    
    if response.status_code == 200:
        message_data = response.json()
        text = message_data.get('text', '').lower()
        print(f"[DEBUG] Message API response text: '{text}'")  # Debug line
        return text
    else:
        print(f"[ERROR] Failed to fetch message: {response.status_code}, {response.text}")
        return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
