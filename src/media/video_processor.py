import yt_dlp
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pathlib import Path
import random
from datetime import datetime

from src.utils.logger import logger
from src.config.settings import (
    VIDEO_ASSETS_DIR,
    TEMP_DIR,
    VIDEO_LENGTH,
    VIDEO_RESOLUTION,
    VIDEO_FPS
)
from src.utils.content_fetcher import ContentFetcher

class VideoProcessor:
    def __init__(self):
        self.temp_dir = TEMP_DIR
        self.assets_dir = VIDEO_ASSETS_DIR
        self.content_fetcher = ContentFetcher()
        
        self.temp_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)

    def download_video(self, url):
        """Download a video from YouTube or other supported platforms"""
        try:
            logger.info(f"Downloading video from: {url}")
            
            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.assets_dir / f"cafe_video_{timestamp}.mp4"
            
            ydl_opts = {
                'format': f'bestvideo[height<={VIDEO_RESOLUTION[1]}]',
                'outtmpl': str(output_path),
                'progress_hooks': [self._download_progress_hook],
                'quiet': False,
                'no_warnings': False
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.debug("Starting download...")
                ydl.download([url])

            if not output_path.exists():
                raise FileNotFoundError(f"Download failed: {output_path} not found")

            logger.info(f"✓ Video downloaded successfully to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"❌ Video download failed: {str(e)}")
            raise

    def _download_progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            try:
                percent = d['_percent_str'].strip()
                logger.debug(f"Download progress: {percent}")
            except KeyError:
                pass
        elif d['status'] == 'finished':
            logger.info("Download completed, processing video...")

    def process_video(self, video_path):
        """Process a video for the study session"""
        try:
            logger.info(f"Processing video: {video_path}")
            
            # Load the video
            video = VideoFileClip(str(video_path))
            
            # Resize if necessary
            if video.size != VIDEO_RESOLUTION:
                logger.info("Resizing video to target resolution...")
                video = video.resize(VIDEO_RESOLUTION)
            
            # Calculate number of loops needed
            duration = video.duration
            loops_needed = int(VIDEO_LENGTH / duration) + 1
            logger.info(f"Video duration: {duration}s, needs {loops_needed} loops")
            
            # Create seamless loop
            logger.info("Creating video loop...")
            clips = [video] * loops_needed
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Trim to exact length
            logger.info("Trimming to final length...")
            final_video = final_video.subclip(0, VIDEO_LENGTH)
            
            # Prepare output path
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.temp_dir / f"processed_video_{timestamp}.mp4"
            
            # Write final video
            logger.info("Writing processed video...")
            final_video.write_videofile(
                str(output_path),
                fps=VIDEO_FPS,
                codec='libx264',
                audio=False,
                preset='medium',
                threads=4
            )
            
            # Cleanup
            video.close()
            final_video.close()
            
            logger.info(f"✓ Video processing complete: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"❌ Video processing failed: {str(e)}")
            raise
        
    def create_study_video(self, input_video_path=None):
        """Create a complete study video from input or random asset"""
        try:
            # If no input video, use random one from assets
            if input_video_path is None:
                available_videos = list(self.assets_dir.glob('*.mp4'))
                if not available_videos:
                    raise FileNotFoundError("No video assets found!")
                input_video_path = random.choice(available_videos)
                logger.info(f"Selected random video: {input_video_path}")
            
            # Process the video
            processed_video = self.process_video(input_video_path)
            
            return processed_video

        except Exception as e:
            logger.error(f"❌ Study video creation failed: {str(e)}")
            raise 

    def get_video(self):
        """Get a random video from our content sources"""
        try:
            video_info = self.content_fetcher.fetch_random_video()
            video_path = self.download_video(video_info['url'])
            return video_path
        except Exception as e:
            logger.error(f"❌ Error getting video: {str(e)}")
            raise 