import logging
import os
import time
import uuid
import random
from io import BytesIO, StringIO
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone

# Python 3.10+ compatibility fix
import collections
try:
    from collections.abc import Mapping, MutableMapping, Iterable, MutableSet, Callable
    collections.Mapping = Mapping
    collections.MutableMapping = MutableMapping
    collections.Iterable = Iterable
    collections.MutableSet = MutableSet
    collections.Callable = Callable
    print("✅ Python 3.10+ compatibility fix applied!")
except ImportError:
    print("⚠️ Using older Python version")

from dotenv import load_dotenv
from pyrogram import Client

botStartTime = time.time()

# Environment loading
if os.path.exists('VideoEncoder/config.env'):
    load_dotenv('VideoEncoder/config.env')

# ULTIMATE TIME SYNC FIX - Force time reference
def force_time_sync():
    """Ultimate time synchronization fix"""
    try:
        # Force UTC with multiple methods
        os.environ['TZ'] = 'UTC'
        time.tzset()
        
        # Force current time reference
        current_utc = datetime.now(timezone.utc)
        current_timestamp = int(current_utc.timestamp())
        
        print(f"🕐 Forced UTC Time: {current_utc}")
        print(f"🕐 Timestamp: {current_timestamp}")
        
        # Add small random delay to avoid exact timing conflicts
        time.sleep(random.uniform(1, 3))
        
        return current_timestamp
    except Exception as e:
        print(f"⚠️ Time sync error: {e}")
        return int(time.time())

# Execute ultimate time sync
sync_timestamp = force_time_sync()

# Variables with your original values
api_id = int(os.environ.get("API_ID", "24828197"))
api_hash = os.environ.get("API_HASH", "d36e278e89ebeb900aeda4128d413a77")
bot_token = os.environ.get("BOT_TOKEN", "7685081691:AAFhcrRMYsuoYNRoFz-mgpzElLIdvHVeTsU")

database = os.environ.get("MONGO_URI", "mongodb+srv://Krishna:krishna@cluster0.ecime.mongodb.net/")

# COMPLETELY UNIQUE session name - timestamp + random + process ID
session_base = os.environ.get("SESSION_NAME", "encoderbot")
session = f"{session_base}_{sync_timestamp}_{random.randint(10000,99999)}_{os.getpid()}"

drive_dir = os.environ.get("DRIVE_DIR", "")
index = os.environ.get("INDEX_URL", "")

download_dir = os.environ.get("DOWNLOAD_DIR", "VideoEncoder/downloads/")
encode_dir = os.environ.get("ENCODE_DIR", "VideoEncoder/encodes/")

owner = list(set(int(x) for x in os.environ.get("OWNER_ID", "7660990923").split() if x.strip()))
sudo_users = list(set(int(x) for x in os.environ.get("SUDO_USERS", "2089948673").split() if x.strip()))
everyone = list(set(int(x) for x in os.environ.get("EVERYONE_CHATS", "-1002775838126").split() if x.strip()))
all = everyone + sudo_users + owner

try:
    log = int(os.environ.get("LOG_CHANNEL", "-1002659515511"))
except:
    log = owner[0] if owner else 7660990923
    print('Using owner as log channel!')

data = []

PROGRESS = """
• {0} of {1}
• Speed: {2}
• ETA: {3}
"""

video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]

def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode()
    file = BytesIO() if bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file

# Check and create folders
for directory in [download_dir, encode_dir]:
    if not os.path.isdir(directory):
        os.makedirs(directory)
        print(f"📁 Created directory: {directory}")

# Enhanced logging setup
log_dir = 'VideoEncoder/utils/extras'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            f'{log_dir}/logs.txt',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

print(f"🔧 Using unique session: {session}")

# ULTIMATE CLIENT - Minimal configuration for maximum compatibility
app = Client(
    session,
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
    plugins={'root': os.path.join(__package__, 'plugins')}
    # NO other parameters to avoid conflicts
)

print("✅ Client initialized with minimal config!")
print(f"📊 Config loaded - Owner: {len(owner)}, Sudo: {len(sudo_users)}, Everyone: {len(everyone)}")
