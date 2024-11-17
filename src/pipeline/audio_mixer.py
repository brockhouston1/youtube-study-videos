from pathlib import Path
import subprocess
from typing import Optional
from src.utils.logger import logger
from src.config.settings import MUSIC_DIR, OUTPUT_DIR

class AudioMixer:
    def __init__(self):
        self.output_dir = OUTPUT_DIR / "final_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def combine_video_and_audio(
        self,
        video_path: Path,
        audio_path: Path,
        output_filename: str,
        volume: float = 1.0
    ) -> Optional[Path]:
        """Combine video with audio track"""
        try:
            output_path = self.output_dir / output_filename
            
            logger.info(f"\nCombining video and audio:")
            logger.info(f"Video: {video_path.name}")
            logger.info(f"Audio: {audio_path.name}")
            
            # FFmpeg command to combine video and audio
            cmd = [
                'ffmpeg',
                '-i', str(video_path),  # Video input
                '-stream_loop', '-1',   # Loop the audio indefinitely
                '-i', str(audio_path),  # Audio input
                '-c:v', 'copy',         # Copy video stream without re-encoding
                '-c:a', 'aac',          # Audio codec
                '-filter:a', f'volume={volume}',  # Adjust volume
                '-t', '3600',           # Set the duration to 1 hour
                '-y',                   # Overwrite output if exists
                str(output_path)
            ]
            
            # Run FFmpeg
            logger.info("\nProcessing... This may take a few minutes.")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"\n✓ Successfully created: {output_path.name}")
                return output_path
            else:
                logger.error(f"FFmpeg Error: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to combine video and audio: {str(e)}")
            return None 