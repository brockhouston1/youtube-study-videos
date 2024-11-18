import os
import yt_dlp
from moviepy.editor import AudioFileClip

def download_audio(playlist_url, num_videos, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': os.path.join(output_folder, 'audio_%(playlist_index)s.mp3'),
        'noplaylist': False,
        'progress_hooks': [hook],
        'concurrent_fragments': 5,  # Number of concurrent downloads
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['filename']} - {d['_percent_str']} - {d['_eta_str']} remaining")

def split_audio(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.mp3'):
            audio_path = os.path.join(input_folder, filename)
            print(f'Splitting audio: {filename}')
            with AudioFileClip(audio_path) as audio:
                duration = int(audio.duration)  # Duration in seconds
                for start in range(0, duration, 3600):  # 3600 seconds = 1 hour
                    end = min(start + 3600, duration)
                    chunk = audio.subclip(start, end)
                    chunk_filename = os.path.join(output_folder, f'{filename[:-4]}_chunk_{start // 60 + 1}.mp3')
                    chunk.write_audiofile(chunk_filename, codec='mp3')
                    print(f'Created chunk: {chunk_filename}')

def main():
    playlist_url = 'https://www.youtube.com/watch?v=4RzaFA4xS9o&list=PLOmXeJ5JdDWU3UZssX-7QRxl9jht-lCp5'  # Replace with your playlist URL
    num_videos = 60
    output_folder = 'assets/music'  # Temporary folder for downloaded audio
    hour_videos_folder = 'assets/hour_videos'  # Folder for hour-long chunks

    # Create output folders
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(hour_videos_folder, exist_ok=True)

    # Download audio
    download_audio(playlist_url, num_videos, output_folder)

    # Split audio into 1-hour chunks
    split_audio(output_folder, hour_videos_folder)

    # Clean up downloaded audio
    for filename in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, filename))
    os.rmdir(output_folder)

if __name__ == '__main__':
    main() 