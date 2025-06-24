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
            
        # Respond to a command (e.g., "summary")
        text = data.get('data', {}).get('text', '').lower()
        room_id = data.get('data', {}).get('roomId', '')
        
        print(f"[DEBUG] Text received: '{text}'")  # Debug line
        print(f"[DEBUG] Room ID: {room_id}")  # Debug line
        
        if not room_id:
            return jsonify({'status': 'error', 'message': 'No room ID provided'}), 400
            
        if 'summary' in text or 'report' in text:
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
            print(f"[DEBUG] No summary/report found in text: '{text}'")  # Debug line
            send_message(room_id, '👋 Hi! Send "summary" or "report" to get your Webex activity summary.')
            
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500
