import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Access environment variables

GOOGLE_API_JSON_PATH = os.getenv('GOOGLE_API_JSON_PATH')
MOODLE_TOKEN = os.getenv('MOODLE_TOKEN')
MOODLE_BASE_URL = os.getenv('MOODLE_BASE_URL')
ADMIN_MAIL = os.getenv('ADMIN_MAIL')


SMS_MS = os.getenv('SMS_MS')
NOTIFICATION_MS = os.getenv('NOTIFICATION_MS')
ACTIVITY_MS = os.getenv('ACTIVITY_MS')