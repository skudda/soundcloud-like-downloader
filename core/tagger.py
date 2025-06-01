import requests
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, error
from mutagen.mp3 import MP3

def tag_mp3(file_path, title, artist, album, artwork_url):
    try:
        audio = MP3(file_path, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass

        audio.tags.add(TIT2(encoding=3, text=title))
        audio.tags.add(TPE1(encoding=3, text=artist))
        if album:
            audio.tags.add(TALB(encoding=3, text=album))

        if artwork_url:
            artwork_url = artwork_url.replace('-large', '-t500x500')
            img_data = requests.get(artwork_url).content
            audio.tags.add(APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc='Cover',
                data=img_data
            ))

        audio.save()
        print(f"🎨 Tagged: {title}")
    except Exception as e:
        print(f"⚠️ Failed to tag {title}: {e}")
