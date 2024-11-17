from src.generators.image_generator import ImageGenerator
from src.utils.logger import logger
from src.config.settings import SCENE_VARIATIONS
import os
import time

def test_multiple_scenes():
    logger.info("=== Testing Reliability of Cozy Scene Generation ===")
    
    try:
        generator = ImageGenerator()
        
        # Test base scene 3 times
        logger.info("\nGenerating 3 base scenes...")
        
        for i in range(3):
            logger.info(f"\nTest {i + 1}/3:")
            image_path = generator.generate_scene()
            
            if image_path and os.path.exists(image_path):
                size_mb = os.path.getsize(image_path) / (1024 * 1024)
                logger.info(f"✓ Scene generated successfully!")
                logger.info(f"Location: {image_path}")
                logger.info(f"Size: {size_mb:.2f} MB")
                
                # Small delay between generations
                time.sleep(2)
            else:
                logger.error(f"Failed to generate scene {i + 1}")
        
        logger.info("\n✓ Reliability test completed!")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_multiple_scenes() 