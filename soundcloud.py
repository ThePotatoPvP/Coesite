import yt_dlp
from audio import get_audio_quality, order

def search_soundcloud(query, num_results=3):
    ydl_opts = {
        'default_search': 'sc',  # This will make it search SoundCloud
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',
        'format': 'bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f'scsearch{num_results}:{query}', download=False)

    results = []
    for entry in search_results['entries']:
        video_name = entry['title']
        channel_name = entry['uploader']
        url = entry['webpage_url']
        audio_quality = get_audio_quality(url)

        result = {
            'video_name': video_name,
            'channel_name': channel_name,
            'url': url,
            'audio_quality': audio_quality
        }
        results.append(result)

    return results

if __name__ == "__main__":
    print(search_soundcloud("jaira burns"))