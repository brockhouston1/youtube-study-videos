from src.utils.logger import logger
from src.config import settings

def test_settings():
    logger.info("=== Testing Settings ===")
    
    try:
        # Verify settings loads correctly
        settings.verify_settings()
        
        # Test critical paths
        logger.info("Checking critical paths...")
        paths_to_check = [
            settings.BASE_DIR,
            settings.ASSETS_DIR,
            settings.OUTPUT_DIR,
            settings.LOGS_DIR,
            settings.VIDEO_ASSETS_DIR,
            settings.MUSIC_ASSETS_DIR
        ]
        
        for path in paths_to_check:
            if path.exists():
                logger.info(f"✓ {path.name} directory exists")
            else:
                logger.error(f"❌ {path.name} directory not found!")
        
        logger.info("=== Settings Test Complete ===")
        
    except Exception as e:
        logger.error(f"Settings test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_settings() 