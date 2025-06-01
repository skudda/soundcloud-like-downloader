import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get and sanitize values
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN", "").strip().strip("'\"")
SC_USERNAME = os.getenv("SC_USERNAME", "").strip().strip("'\"")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output").strip()
MUSIC_DIR = os.path.join(OUTPUT_DIR, os.getenv("MUSIC_DIR", "music").strip())


# Validate config
if not OAUTH_TOKEN or not OAUTH_TOKEN.startswith("2-"):
    raise ValueError("❌ Invalid or missing OAUTH_TOKEN in .env file. Make sure it's unquoted and starts with 2-")

if not SC_USERNAME:
    raise ValueError("❌ USERNAME is missing or incorrectly formatted in .env")

# Optional: create download folder if it doesn't exist
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)
    print(f"📂 Created download directory: {MUSIC_DIR}")

# Set headers
HEADERS = {
    'Authorization': f'OAuth {OAUTH_TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://soundcloud.com/',
}
