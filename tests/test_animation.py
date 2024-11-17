from src.generators.image_generator import ImageGenerator
from src.generators.animation_creator import AnimationCreator
from src.utils.logger import logger
import os
import time

def test_steam_animation():
    logger.info("=== Testing Steam Animation Effect ===")
    
    try:
        # Generate a scene
        image_generator = ImageGenerator()
        image_path = image_generator.generate_scene(
            "with a steaming hot coffee cup on the wooden table"
        )
        
        if not image_path:
            raise ValueError("Failed to generate base image")
        
        # Create animation
        logger.info("\nCreating steam animation...")
        start_time = time.time()
        
        animator = AnimationCreator()
        animation_path = animator.create_animation(image_path)
        
        if animation_path and os.path.exists(animation_path):
            duration = time.time() - start_time
            size_mb = os.path.getsize(animation_path) / (1024 * 1024)
            logger.info(f"\n✓ Steam animation created successfully!")
            logger.info(f"Location: {animation_path}")
            logger.info(f"Size: {size_mb:.2f} MB")
            logger.info(f"Generation time: {duration:.2f} seconds")
            
            logger.info("\nYou should now see:")
            logger.info("1. Gentle steam rising from the coffee cup")
            logger.info("2. Soft, wavy motion in the steam")
            logger.info("3. Gradual fade-out as steam rises")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_steam_animation() 