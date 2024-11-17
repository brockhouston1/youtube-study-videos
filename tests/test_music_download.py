from src.music.download_tracks import setup_music_library
from src.config.settings import MUSIC_DIR
from src.utils.logger import logger
import os

def test_music_download():
    logger.info("=== Testing Music Library Setup ===")
    
    try:
        # Setup music library
        setup_music_library()
        
        # Verify downloads
        expected_files = [
            'lofi_study.mp3',
            'ambient_chill.mp3',
            'cafe_ambience.mp3',
            'metadata.json'
        ]
        
        for filename in expected_files:
            filepath = MUSIC_DIR / filename
            if filepath.exists():
                size_mb = filepath.stat().st_size / (1024 * 1024)
                logger.info(f"✓ {filename}: {size_mb:.2f} MB")
            else:
                logger.error(f"❌ Missing file: {filename}")
                raise FileNotFoundError(f"Missing file: {filename}")
        
        logger.info("\n✓ Music library setup complete!")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_music_download() 