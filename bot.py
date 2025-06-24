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
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
            
        # Ignore messages sent by the bot itself
        if data.get('data', {}).get('personEmail') == os.getenv('BOT_USERNAME', ''):
            return jsonify({'status': 'ignored'}), 200
            
        # Respond to a command (e.g., "summary")
        text = data.get('data', {}).get('text', '').lower()
        room_id = data.get('data', {}).get('roomId', '')
        
        if not room_id:
            return jsonify({'status': 'error', 'message': 'No room ID provided'}), 400
            
        if 'summary' in text or 'report' in text:
            try:
                send_message(room_id, '🔄 Generating your Webex activity report... This may take a moment.')
                file_path = generate_report()
                send_message(room_id, '✅ Webex summary report generated! See attached HTML file.')
                send_file(room_id, file_path)
            except Exception as e:
                print(f"[ERROR] Failed to generate report: {e}")
                send_message(room_id, f'❌ Sorry, I encountered an error generating the report: {str(e)}')
        else:
            send_message(room_id, '👋 Hi! Send "summary" or "report" to get your Webex activity summary.')
            
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
