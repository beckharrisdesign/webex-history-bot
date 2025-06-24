import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)  # Force reload to get updated values

# Load sensitive info from environment variables for security
ACCESS_TOKEN = os.getenv('WEBEX_ACCESS_TOKEN', '')
ORG_ID = os.getenv('WEBEX_ORG_ID', '')

# Constants
MAX_MESSAGES = 10
MAX_ROOMS_PER_PAGE = 50  # Increased from 5 for production use
IGNORE_LIST = [
    'Adult Caregivers Network',
    'BridgeIT Support Space',
    'BridgeIT API - Support - https://eurl.io/#2PnHT3YSf',
    'AI / NLP - Technology Discussions - https://eurl.io/#46ICOhHFI',
    'CETO Jira FAQ and Chat https://eurl.io/#EvbGrgkbG'
]