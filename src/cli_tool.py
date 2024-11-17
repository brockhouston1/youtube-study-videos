import argparse
from src.pipeline.study_video_creator import StudyVideoCreator
from src.music.youtube_music_fetcher import MusicFetcher
from src.pipeline.audio_mixer import AudioMixer
from src.youtube_uploader import upload_video, authenticate_youtube

def generate_video():
    """Generate a study video."""
    print("Generating video...")

    # Initialize components
    video_creator = StudyVideoCreator()
    music_fetcher = MusicFetcher()
    audio_mixer = AudioMixer()

    # Fetch and download music
    track_key = 'cozy_winter'
    print("Downloading music track...")
    full_track_path = music_fetcher.download_long_track(track_key)

    # Create video
    print("Creating video...")
    video_path = video_creator.create_study_video()

    # Mix audio with video
    if video_path and full_track_path:
        print("Mixing audio with video...")
        final_video_path = audio_mixer.combine_video_and_audio(
            video_path=video_path,
            audio_path=full_track_path,
            output_filename="final_study_video.mp4",
            volume=0.85
        )
        if final_video_path:
            print(f"Video created at: {final_video_path}")
        else:
            print("Failed to mix audio with video.")
    else:
        print("Failed to create video or download music.")

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