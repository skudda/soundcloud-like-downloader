import os
import time
import requests
from config import HEADERS, MUSIC_DIR, OUTPUT_DIR
from tagger import tag_mp3
from utils import sanitize_filename

def download_track(track):
    artist = track['user']['username']
    title = sanitize_filename(f"{artist} - {track['title']}")
    file_path = os.path.join(MUSIC_DIR, f"{title}.mp3")

    if os.path.exists(file_path):
        return 'skipped'

    transcodings = track.get('media', {}).get('transcodings', [])
    progressive = next((t for t in transcodings if 'progressive' in t['format']['protocol']), None)

    if not progressive:
        print(f"⚠️ Only HLS stream found (label-restricted): {title}")
        with open(os.path.join(OUTPUT_DIR, "skipped_hls.txt"), "a", encoding="utf-8") as log:
            log.write(f"{title} - Skipped: HLS only\n")
        return

    stream_url = progressive['url']
    retries = 3
    while retries > 0:
        try:
            r = requests.get(stream_url, headers=HEADERS, timeout=(5, 15))
            actual_url = r.json().get('url')
            if not actual_url:
                print(f"❌ No stream URL for {title}. Retrying...")
                time.sleep(10)
                retries -= 1
                continue

            r = requests.get(actual_url, stream=True, timeout=(5, 30))
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"🎵 Downloaded: {title}")

            publisher_data = track.get('publisher_metadata') or {}
            album = publisher_data.get('release_title', '')

            tag_mp3(
                file_path,
                title=track['title'],
                artist=artist,
                album=album,
                artwork_url=track.get('artwork_url')
            )
            return
        except Exception as e:
            print(f"⚠️ Temporary issue with {title}: {e}")
            print(f"🔁 Retrying... ({4 - retries}/3)")
            time.sleep(10)
            retries -= 1

    print(f"❌ Giving up on: {title}")
    with open(os.path.join(OUTPUT_DIR, "failed-downloads.txt"), "a", encoding="utf-8") as log:
        log.write(f"{title} - Failed after retries\n")
