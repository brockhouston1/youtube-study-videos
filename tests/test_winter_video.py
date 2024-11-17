from src.music.youtube_music_fetcher import MusicFetcher
from src.pipeline.study_video_creator import StudyVideoCreator
from src.pipeline.audio_mixer import AudioMixer
from src.utils.logger import logger
from src.config.settings import MUSIC_DIR
import subprocess
from pathlib import Path

def create_winter_study_video():
    logger.info("=== Creating Cozy Winter Study Video ===")
    
    try:
        # 1. Download the winter track
        fetcher = MusicFetcher()
        track_key = 'cozy_winter'
        
        logger.info(f"\n1. Downloading winter lofi track...")
        full_track_path = fetcher.download_long_track(track_key)
        
        if not full_track_path:
            raise ValueError("Failed to download track")
            
        # 2. Cut the track to 1 hour
        logger.info("\n2. Trimming track to 1 hour...")
        trimmed_track_path = MUSIC_DIR / "winter_1hour.mp3"
        
        trim_cmd = [
            'ffmpeg',
            '-i', str(full_track_path),
            '-t', '3600',  # 1 hour in seconds
            '-c:a', 'libmp3lame',
            '-q:a', '2',  # High quality
            '-y',  # Overwrite if exists
            str(trimmed_track_path)
        ]
        
        result = subprocess.run(trim_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise ValueError(f"Failed to trim audio: {result.stderr}")
            
        logger.info("✓ Track trimmed successfully")
        
        # 3. Create the study video
        logger.info("\n3. Creating study video...")
        video_creator = StudyVideoCreator()
        
        # Optional: Add winter-specific prompt
        winter_prompt = """Create a cozy winter study scene with a warm coffee shop interior. 
        Show large windows with gentle snowfall outside, soft warm lighting inside, 
        and comfortable seating areas with books and laptops. Include fairy lights 
        and holiday decorations tastefully placed around the space."""
        
        video_path = video_creator.create_study_video(prompt=winter_prompt)
        
        if not video_path:
            raise ValueError("Failed to create video")
            
        # 4. Combine video and trimmed audio
        logger.info("\n4. Combining video and audio...")
        mixer = AudioMixer()
        
        final_video = mixer.combine_video_and_audio(
            video_path=video_path,
            audio_path=trimmed_track_path,
            output_filename="winter_study_session.mp4",
            volume=0.85  # Slightly reduced volume
        )
        
        if final_video and final_video.exists():
            size_mb = final_video.stat().st_size / (1024 * 1024)
            logger.info(f"\n✓ Winter study video created successfully!")
            logger.info(f"Location: {final_video}")
            logger.info(f"Size: {size_mb:.2f} MB")
            logger.info(f"Duration: 1 hour")
            return final_video
        else:
            raise ValueError("Failed to create final video")
        
    except Exception as e:
        logger.error(f"\n❌ Process failed: {str(e)}")
        raise

if __name__ == "__main__":
    create_winter_study_video() 