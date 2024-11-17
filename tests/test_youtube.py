from src.utils.youtube import YouTubeUploader
from src.utils.logger import logger
import os

def test_youtube_auth():
    logger.info("=== Testing YouTube Authentication ===")
    try:
        uploader = YouTubeUploader()
        logger.info("✓ Authentication successful")
        return uploader
    except Exception as e:
        logger.error(f"❌ Authentication failed: {str(e)}")
        raise

def test_upload(uploader, test_video_path):
    logger.info("=== Testing Video Upload ===")
    try:
        # Upload video as private
        video_id = uploader.upload_video(test_video_path)
        logger.info(f"✓ Upload successful. Video ID: {video_id}")
        return video_id
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        raise

if __name__ == "__main__":
    # This is just a basic test - we'll need an actual video file for upload testing
    uploader = test_youtube_auth()
    logger.info("YouTube API connection established successfully!") 