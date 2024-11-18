import os
import yt_dlp

def download_audio(playlist_url, num_videos, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': os.path.join(output_folder, 'audio_%(playlist_index)s.%(ext)s'),
        'noplaylist': False,
        'progress_hooks': [hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['filename']} - {d['_percent_str']} - {d['_eta_str']} remaining")

def main():
    playlist_url = 'https://www.youtube.com/watch?v=4RzaFA4xS9o&list=PLOmXeJ5JdDWU3UZssX-7QRxl9jht-lCp5'  # Replace with your playlist URL
    num_videos = 60
    output_folder = 'assets/music'  # Temporary folder for downloaded audio

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    # Download audio
    download_audio(playlist_url, num_videos, output_folder)

if __name__ == '__main__':
    main()
