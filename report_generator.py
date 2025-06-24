from datetime import datetime, timezone, timedelta
import os

# Handle both relative and absolute imports
try:
    from .api import fetch_rooms, filter_active_rooms
    from .html_report import generate_html
    from .config import IGNORE_LIST
except ImportError:
    from api import fetch_rooms, filter_active_rooms
    from html_report import generate_html
    from config import IGNORE_LIST

def generate_report():
    """
    Main function to generate a Webex activity report.
    Returns the file path of the generated HTML report.
    """
    try:
        # Get current time and calculate one week ago
        now = datetime.now(timezone.utc)
        one_week_ago = now - timedelta(days=7)
        
        print("[INFO] Fetching rooms...")
        rooms = fetch_rooms(max_rooms_per_page=50)  # Increased for production
        print(f"[INFO] Fetched {len(rooms)} total rooms")
        
        # Filter rooms for active ones in the last week
        active_rooms = filter_active_rooms(rooms, IGNORE_LIST, one_week_ago, now)
        print(f"[INFO] Found {len(active_rooms)} active rooms in the last 7 days")
        
        # Sort by last activity (most recent first)
        active_rooms.sort(key=lambda x: x.get('lastActivity', ''), reverse=True)
        
        # Generate HTML report
        html_content = generate_html(active_rooms, now)
        
        # Save to file
        output_file = "webex_recent_rooms.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[INFO] Report generated: {output_file}")
        return os.path.abspath(output_file)
        
    except Exception as e:
        print(f"[ERROR] Failed to generate report: {str(e)}")
        raise e