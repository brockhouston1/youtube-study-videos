from src.generators.image_generator import ImageGenerator
from src.utils.logger import logger
from src.config.settings import BASE_PROMPT, SCENE_VARIATIONS
import os

def test_cafe_scene():
    logger.info("=== Testing Cozy Cafe Scene Generation ===")
    
    try:
        generator = ImageGenerator()
        
        # Generate base scene
        logger.info("\nGenerating cozy cafe scene...")
        logger.info("\nUsing base prompt:")
        logger.info(BASE_PROMPT)
        
        image_path = generator.generate_scene()
        
        if image_path and os.path.exists(image_path):
            logger.info(f"\n✓ Scene generated successfully!")
            logger.info(f"Location: {image_path}")
            
            # Log file details
            size_mb = os.path.getsize(image_path) / (1024 * 1024)
            logger.info(f"File size: {size_mb:.2f} MB")
            
        # Try a rainy variation
        variation = SCENE_VARIATIONS[0]  # Get the first variation
        logger.info(f"\nTrying variation: {variation}")
        
        var_image_path = generator.generate_scene(variation)
        
        if var_image_path and os.path.exists(var_image_path):
            logger.info(f"\n✓ Variation scene generated successfully!")
            logger.info(f"Location: {var_image_path}")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_cafe_scene() 