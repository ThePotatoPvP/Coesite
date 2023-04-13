import yt_dlp
import os

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
