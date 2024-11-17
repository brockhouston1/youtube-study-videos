from src.generators.image_generator import ImageGenerator
from src.generators.video_creator import VideoCreator
from src.utils.logger import logger
import os
import time

def test_video_creation():
    logger.info("=== Testing Short Loopable Video Creation ===")
    
    try:
        # First generate a scene
        image_generator = ImageGenerator()
        image_path = image_generator.generate_scene()
        
        if not image_path:
            raise ValueError("Failed to generate base image")
            
        logger.info(f"Image generated successfully at: {image_path}")
        
        # Create video
        logger.info("\nCreating loopable video from scene...")
        start_time = time.time()
        
        video_creator = VideoCreator()
        video_path = video_creator.create_video(image_path)
        
        if video_path and os.path.exists(video_path):
            duration = time.time() - start_time
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            logger.info(f"\n✓ Video created successfully!")
            logger.info(f"Location: {video_path}")
            logger.info(f"Size: {size_mb:.2f} MB")
            logger.info(f"Generation time: {duration:.2f} seconds")
            
            logger.info("\nVideo properties:")
            logger.info(f"- Duration: 5 seconds (loopable)")
            logger.info(f"- Resolution: 1920x1080")
            logger.info(f"- FPS: 30")
            logger.info("\nTo use: Set your video player to loop this short video")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_video_creation() 