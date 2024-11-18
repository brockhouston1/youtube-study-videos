from pathlib import Path
import subprocess
from typing import Optional
from src.utils.logger import logger
from src.config.settings import OUTPUT_DIR
from src.generators.image_generator import ImageGenerator

class StudyVideoCreator:
    def __init__(self):
        self.output_dir = OUTPUT_DIR / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.image_generator = ImageGenerator()
        
    def create_study_video(self, prompt: Optional[str] = None) -> Optional[Path]:
        """Create a study video from an image, optionally using a custom prompt"""
        try:
            # Use custom prompt if provided, otherwise let generate_scene use default
            if prompt:
                image_path = self.image_generator.generate_scene(variation=prompt)
            else:
                image_path = self.image_generator.generate_scene()
            
            if not image_path or not image_path.exists():
                raise ValueError("Failed to generate image or image does not exist")
            
            logger.info(f"Generated image at: {image_path}")

            # Create a short 10-second video from the image
            short_video_path = self.output_dir / "short_study_video.mp4"
            cmd_short = [
                'ffmpeg',
                '-loop', '1',
                '-i', str(image_path),
                '-c:v', 'libx264',  # Use libx264 for compatibility
                '-preset', 'fast',  # Use a faster preset
                '-tune', 'stillimage',
                '-pix_fmt', 'yuv420p',
                '-t', '10',  # 10 seconds duration
                '-vf', 'scale=1920:1080',
                '-y',
                str(short_video_path)
            ]
            
            logger.info("Creating 10-second video segment...")
            result_short = subprocess.run(cmd_short, capture_output=True, text=True)
            
            if result_short.returncode != 0:
                logger.error(f"FFmpeg Error (short video): {result_short.stderr}")
                return None
            
            logger.info(f"✓ Short video created: {short_video_path}")

            # Loop the 10-second video to create a 1-hour video
            final_video_path = self.output_dir / "study_video.mp4"
            cmd_final = [
                'ffmpeg',
                '-stream_loop', '-1',  # Loop indefinitely
                '-i', str(short_video_path),
                '-c', 'copy',  # Copy streams without re-encoding
                '-t', '3600',  # 1 hour duration
                '-y',
                str(final_video_path)
            ]
            
            logger.info("Creating 1-hour video by looping the short segment...")
            result_final = subprocess.run(cmd_final, capture_output=True, text=True)
            
            if result_final.returncode == 0:
                logger.info(f"✓ Video created: {final_video_path}")
                return final_video_path
            else:
                logger.error(f"FFmpeg Error (final video): {result_final.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create study video: {str(e)}")
            return None 