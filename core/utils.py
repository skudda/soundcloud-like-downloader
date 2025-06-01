import re
import os

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
