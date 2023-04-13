import yt_dlp

def get_audio_quality(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    audio_bitrate = info['abr'] if 'abr' in info else None
    return f'{audio_bitrate} kbps' if audio_bitrate else 'Unknown'

def order(results):
    return sorted(results, key=lambda result: result['audio_quality'] if result['audio_quality'] != 'Unknown' else 0, reverse=True)