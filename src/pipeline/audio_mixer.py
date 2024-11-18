from pathlib import Path
import subprocess
from typing import Optional
from src.utils.logger import logger
from src.config.settings import MUSIC_DIR, OUTPUT_DIR
import os

class AudioMixer:
    def __init__(self):
        self.output_dir = OUTPUT_DIR / "final_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_audio_duration(self, audio_path: Path) -> float:
        """Get the duration of the audio file in seconds using FFprobe."""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            logger.error(f"Failed to get audio duration: {result.stderr}")
            return 0.0

    def combine_video_and_audio(
        self,
        video_path: Path,
        audio_path: Path,
        output_filename: str,
        volume: float = 1.0
    ) -> Optional[Path]:
        """Combine video with audio track, trimming or looping audio as needed."""
        try:
            output_path = self.output_dir / output_filename
            
            logger.info(f"\nCombining video and audio:")
            logger.info(f"Video: {video_path.name}")
            logger.info(f"Audio: {audio_path.name}")
            
            # Get the duration of the audio file
            audio_duration = self.get_audio_duration(audio_path)
            video_duration = 3600  # 1 hour in seconds

            if audio_duration > video_duration:
                # Trim the audio to match the video duration
                logger.info("Trimming audio to match video duration.")
                cmd = [
                    'ffmpeg',
                    '-i', str(video_path),  # Video input
                    '-i', str(audio_path),  # Audio input
                    '-c:v', 'copy',         # Copy video stream without re-encoding
                    '-c:a', 'aac',          # Audio codec
                    '-filter:a', f'volume={volume}',  # Adjust volume
                    '-t', str(video_duration),  # Set the duration to 1 hour
                    '-y',                   # Overwrite output if exists
                    str(output_path)
                ]
            else:
                # Loop the audio to match the video duration
                logger.info("Looping audio to match video duration.")
                cmd = [
                    'ffmpeg',
                    '-i', str(video_path),  # Video input
                    '-stream_loop', '-1',   # Loop the audio indefinitely
                    '-i', str(audio_path),  # Audio input
                    '-c:v', 'copy',         # Copy video stream without re-encoding
                    '-c:a', 'aac',          # Audio codec
                    '-filter:a', f'volume={volume}',  # Adjust volume
                    '-t', str(video_duration),  # Set the duration to 1 hour
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