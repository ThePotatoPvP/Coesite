from youtubesearchpython import VideosSearch
from audio import get_audio_quality, order

def search_youtube(query, num_results=3):
    videos_search = VideosSearch(query, limit=num_results)
    search_results = videos_search.result()

    results = []
    for entry in search_results['result']:
        video_name = entry['title']
        channel_name = entry['channel']['name']
        url = entry['link']
        audio_quality = get_audio_quality(url)
        
        result = {
            'video_name': video_name,
            'channel_name': channel_name,
            'url': url,
            'audio_quality': audio_quality
        }
        results.append(result)

    return results