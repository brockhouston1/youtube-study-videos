from pathlib import Path
import subprocess
from typing import Union
import shutil

from src.utils.logger import logger
from src.config.settings import VIDEO_RESOLUTION, VIDEO_FPS

class VideoCreator:
    def __init__(self):
        self.fps = VIDEO_FPS
        self.resolution = VIDEO_RESOLUTION
        self.duration = 5  # Just 5 seconds, will be looped by video player
        
    def create_video(self, image_path: Union[str, Path]) -> Path:
        """Create a short, loopable video from an image using FFmpeg"""
        try:
            logger.info(f"Creating short loopable video from: {image_path}")
            image_path = Path(image_path)
            
            # Create output path
            output_path = image_path.parent / f"{image_path.stem}_loopable.mp4"
            
            # Construct minimal FFmpeg command
            cmd = [
                'ffmpeg',
                '-loop', '1',
                '-i', str(image_path),
                '-c:v', 'h264_videotoolbox',
                '-tune', 'stillimage',
                '-pix_fmt', 'yuv420p',
                '-t', '3600',
                '-vf', 'scale=1280:720',
                '-y',
                str(output_path)
            ]
            
            logger.info("Creating short loopable video...")
            
            # Run FFmpeg with minimal resources
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            process.wait()
            
            if process.returncode == 0:
                size_mb = output_path.stat().st_size / (1024 * 1024)
                logger.info(f"✓ Loopable video created successfully!")
                logger.info(f"Location: {output_path}")
                logger.info(f"Size: {size_mb:.2f} MB")
                logger.info("\nTo use: Set your video player to loop this short video")
                
                return output_path
            else:
                raise RuntimeError("FFmpeg failed to create video")
            
        except Exception as e:
            logger.error(f"Failed to create video: {str(e)}")
            raise