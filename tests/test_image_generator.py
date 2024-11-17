from src.generators.image_generator import ImageGenerator
from src.utils.logger import logger
import os

def test_image_generator():
    logger.info("=== Testing Image Generator ===")
    
    try:
        # Initialize generator
        generator = ImageGenerator()
        
        # Test with default prompts
        logger.info("\nTesting with default prompt...")
        image_path = generator.generate_scene()
        
        if image_path and os.path.exists(image_path):
            image_size = os.path.getsize(image_path) / (1024 * 1024)  # Size in MB
            logger.info(f"\n✓ Image generated successfully!")
            logger.info(f"Location: {image_path}")
            logger.info(f"Size: {image_size:.2f} MB")
        else:
            logger.error("Failed to generate image with default prompt")
            return
        
        # Test with custom prompt
        custom_prompt = "mideval cafe"
        logger.info(f"\nTesting with custom prompt: {custom_prompt}")
        custom_image_path = generator.generate_scene(custom_prompt)
        
        if custom_image_path and os.path.exists(custom_image_path):
            image_size = os.path.getsize(custom_image_path) / (1024 * 1024)
            logger.info(f"\n✓ Custom image generated successfully!")
            logger.info(f"Location: {custom_image_path}")
            logger.info(f"Size: {image_size:.2f} MB")
        else:
            logger.error("Failed to generate image with custom prompt")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_image_generator() 