from src.pipeline.audio_mixer import AudioMixer
from src.music.youtube_music_fetcher import MusicFetcher
from src.pipeline.study_video_creator import StudyVideoCreator
from src.utils.logger import logger
from pathlib import Path

def test_audio_mixer():
    logger.info("=== Testing Audio Mixer ===")
    
    try:
        # 1. First get our music track
        music_fetcher = MusicFetcher()
        logger.info("\nDownloading test music track...")
        
        # Use a static track for testing
        track_key = 'study_session_1'  # This is our 1-hour track
        audio_path = music_fetcher.download_long_track(track_key)
        
        if not audio_path:
            raise ValueError("Failed to download music track")
        
        # 2. Create our base video
        video_creator = StudyVideoCreator()
        logger.info("\nCreating test video...")
        video_path = video_creator.create_study_video()
        
        if not video_path:
            raise ValueError("Failed to create video")
        
        # 3. Combine video and audio
        mixer = AudioMixer()
        logger.info("\nCombining video and audio...")
        
        final_video = mixer.combine_video_and_audio(
            video_path=video_path,
            audio_path=audio_path,
            output_filename="final_study_video.mp4",
            volume=0.8  # Slightly reduce music volume
        )
        
        if final_video and final_video.exists():
            size_mb = final_video.stat().st_size / (1024 * 1024)
            logger.info(f"\n✓ Final video created successfully!")
            logger.info(f"Location: {final_video}")
            logger.info(f"Size: {size_mb:.2f} MB")
        else:
            raise ValueError("Failed to create final video")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_audio_mixer() 