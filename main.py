import time
import os
from config import SC_USERNAME, MUSIC_DIR
from fetcher import get_user_id, get_likes
from downloader import download_track
from utils import ensure_dir

def main():
    ensure_dir(MUSIC_DIR)

    # 🔍 Detect existing .mp3 files to determine if resuming
    already_downloaded = [
        f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')
    ]
    if already_downloaded:
        print("🔁 Resuming from previous run... already-downloaded tracks will be skipped silently.")

    user_id = get_user_id(SC_USERNAME)
    liked_tracks = get_likes(user_id)
    print(f"🎧 Found {len(liked_tracks)} liked tracks.")

    skipped = 0
    downloaded = 0

    for track in liked_tracks:
        result = download_track(track)

        if result == 'skipped':
            skipped += 1
            continue

        downloaded += 1
        time.sleep(2)

        if downloaded % 100 == 0:
            print("⏳ Cooling down... Sleeping for 60 seconds")
            time.sleep(60)

    print(f"\n✅ Done!")
    print(f"📂 Skipped: {skipped} (already downloaded)")
    print(f"🎧 Downloaded: {downloaded}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user.")
