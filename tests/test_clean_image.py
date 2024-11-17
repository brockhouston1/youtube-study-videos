from src.generators.image_generator import ImageGenerator
from src.utils.logger import logger
import os

def test_clean_image():
    logger.info("=== Testing Clean Image Generation (No Color Palettes) ===")
    
    try:
        generator = ImageGenerator()
        
        logger.info("\nGenerating clean scene...")
        image_path = generator.generate_scene()
        
        if image_path and os.path.exists(image_path):
            size_mb = os.path.getsize(image_path) / (1024 * 1024)
            logger.info(f"\n✓ Scene generated successfully!")
            logger.info(f"Location: {image_path}")
            logger.info(f"Size: {size_mb:.2f} MB")
            
            logger.info("\nPlease verify:")
            logger.info("1. Image shows only the cafe scene")
            logger.info("2. No color palettes or additional elements")
            logger.info("3. Clean, single-frame composition")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_clean_image() 