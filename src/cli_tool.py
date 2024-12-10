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

def generate_and_upload_video():
    """Generate a study video and upload it to YouTube."""
    print("Generating video...")

    # Initialize components
    video_creator = StudyVideoCreator()
    music_directory = 'assets/permuted_tracks_hour'  # Path to your music directory
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
            output_filename="lofi_study_focus_video.mp4",
            volume=0.85
        )
        if final_video_path:
            print(f"Video created at: {final_video_path}")
            # Upload to YouTube
            print("Uploading video to YouTube...")
            youtube_service = authenticate_youtube()
            upload_video(youtube_service, video_file=str(final_video_path))
            print("Upload completed successfully.")
        else:
            print("Failed to mix audio with video.")
    else:
        print("Failed to create video or select audio.")

def main():
    parser = argparse.ArgumentParser(description="Automate study video creation and upload.")
    parser.add_argument('--generate', action='store_true', help="Generate a new study video")
    parser.add_argument('--upload', action='store_true', help="Upload the video to YouTube")
    parser.add_argument('--generate-upload', action='store_true', help="Generate and upload a new study video")
    args = parser.parse_args()

    # if args.generate:
    #     generate_video()

    # if args.upload:
    #     upload_to_youtube()

    if args.generate_upload:
        generate_and_upload_video()

if __name__ == "__main__":
    main() 