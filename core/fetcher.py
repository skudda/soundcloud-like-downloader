import requests
import time
from config import HEADERS

def get_user_id(username):
    url = f'https://api-v2.soundcloud.com/resolve?url=https://soundcloud.com/{username}'
    r = requests.get(url, headers=HEADERS, timeout=(5, 15))
    r.raise_for_status()
    return r.json()['id']

def get_likes(user_id):
    url = f'https://api-v2.soundcloud.com/users/{user_id}/likes?limit=200&offset=0'
    likes = []
    retries = 3

    while url:
        try:
            r = requests.get(url, headers=HEADERS, timeout=(5, 15))
            data = r.json()
            batch = [item['track'] for item in data.get('collection', []) if 'track' in item]
            likes.extend(batch)
            url = data.get('next_href')
        except requests.exceptions.ReadTimeout as e:
            retries -= 1
            if retries > 0:
                print(f"⚠️ Timeout fetching likes. Retrying... ({3 - retries}/3)")
                time.sleep(10)
                continue
            else:
                print("❌ Too many timeouts while fetching likes. Exiting.")
                break
        except Exception as e:
            print(f"❌ Failed to fetch likes: {e}")
            break

    return likes
