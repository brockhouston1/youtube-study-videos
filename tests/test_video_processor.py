from src.media.video_processor import VideoProcessor
from src.utils.logger import logger

def test_video_processor():
    logger.info("=== Testing Video Processor ===")
    
    try:
        processor = VideoProcessor()
        
        # Test automatic video fetching
        logger.info("\nTesting video fetching...")
        video_path = processor.get_video()
        
        # Test video processing
        logger.info("\nTesting video processing...")
        processed_path = processor.process_video(video_path)
        
        logger.info("\n✓ All video processor tests passed!")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_video_processor() 