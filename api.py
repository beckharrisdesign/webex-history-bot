import requests
from datetime import datetime, timezone
from dateutil.parser import isoparse

# Handle both relative and absolute imports
try:
    from .config import ACCESS_TOKEN, MAX_MESSAGES, MAX_ROOMS_PER_PAGE
except ImportError:
    from config import ACCESS_TOKEN, MAX_MESSAGES, MAX_ROOMS_PER_PAGE

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    'Content-Type': 'application/json'
}
ROOMS_URL = "https://webexapis.com/v1/rooms"


def fetch_rooms(max_rooms_per_page=5, headers=HEADERS, rooms_url=ROOMS_URL):
    """
    Fetch rooms that the user is a member of.
    Limited to a small number for testing purposes.
    """
    rooms = []
    url = rooms_url
    # Add type parameter to only get rooms where the user is a member
    # sortBy=lastactivity to get most recently active rooms first
    params = {
        "max": max_rooms_per_page,
        "type": "group",  # Only group rooms (excludes 1:1 conversations)
        "sortBy": "lastactivity"
    }
    
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print(f"[ERROR] Error fetching rooms: {resp.status_code}, Response: {resp.text}")
        return []
    
    data = resp.json()
    rooms = data.get('items', [])
    print(f"[INFO] Fetched {len(rooms)} rooms (limited to {max_rooms_per_page})")
    
    return rooms

def get_message_count(room_id, headers=HEADERS):
    url = f"https://webexapis.com/v1/messages"
    params = {"roomId": room_id, "max": MAX_MESSAGES}
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print(f"[ERROR] Failed to fetch messages for room {room_id}. Status: {resp.status_code}, Response: {resp.text}")
        return 'error'
    messages = resp.json().get('items', [])
    return f"{MAX_MESSAGES}+" if len(messages) == MAX_MESSAGES else len(messages)

def filter_active_rooms(rooms, ignore_list, one_week_ago, now):
    return [
        r for r in rooms
        if r.get('title') not in ignore_list
        and 'lastActivity' in r and r['lastActivity'].startswith('2025')
        and one_week_ago <= isoparse(r['lastActivity']) <= now
    ]
