import os
import random
from pathlib import Path
import argparse
from src.pipeline.study_video_creator import StudyVideoCreator
from src.music.youtube_music_fetcher import MusicFetcher
from src.pipeline.audio_mixer import AudioMixer
from src.youtube_uploader import upload_video, authenticate_youtube

def select_random_audio_file(music_directory: str) -> Path:
    """Select a random audio file from the specified directory."""
    audio_files = [f for f in os.listdir(music_directory) if f.endswith('.mp3')]
    
    if not audio_files:
        raise FileNotFoundError("No audio files found in the specified directory.")
    
    selected_file = random.choice(audio_files)
    return Path(music_directory) / selected_file

def generate_video():
    """Generate a study video."""
    print("Generating video...")

    # Initialize components
    video_creator = StudyVideoCreator()
    music_directory = 'assets/music'  # Path to your music directory
    audio_mixer = AudioMixer()

    # Select a random audio file
    print("Selecting random audio track...")
    selected_audio_path = select_random_audio_file(music_directory)

    # Create video
    print("Creating video...")
    video_path = video_creator.create_study_video()

    # Mix audio with video
    if video_path and selected_audio_path:
        print("Mixing audio with video...")
        final_video_path = audio_mixer.combine_video_and_audio(
            video_path=video_path,
            audio_path=selected_audio_path,
            output_filename="final_study_video.mp4",
            volume=0.85
        )
        if final_video_path:
            print(f"Video created at: {final_video_path}")
        else:
            print("Failed to mix audio with video.")
    else:
        print("Failed to create video or select audio.")

def upload_to_youtube():
    """Upload the video to YouTube."""
    print("Uploading video...")
    youtube_service = authenticate_youtube()
    upload_video(youtube_service, video_file='output/final_videos/final_study_video.mp4')

def main():
    parser = argparse.ArgumentParser(description="Automate study video creation and upload.")
    parser.add_argument('--generate', action='store_true', help="Generate a new study video")
    parser.add_argument('--upload', action='store_true', help="Upload the video to YouTube")
    args = parser.parse_args()

    if args.generate:
        generate_video()

    if args.upload:
        upload_to_youtube()

if __name__ == "__main__":
    main() 