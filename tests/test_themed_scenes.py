from src.generators.image_generator import ImageGenerator
from src.utils.logger import logger
import os

def test_themed_scenes():
    logger.info("=== Testing Medieval Fantasy Cafe Scenes ===")
    
    custom_prompts = [
        "Cozy medieval tavern interior with students studying at ancient wooden tables, magical tomes floating nearby",
        "Wizard's coffee shop with bubbling potion cauldrons and enchanted study nooks, perfect for magical studies",
        "Fantasy library cafe where scrolls float through the air and magical quills take notes automatically"
    ]
    
    try:
        generator = ImageGenerator()
        
        # Test default themed scenes
        logger.info("\nTesting default fantasy cafe scene...")
        default_path = generator.generate_themed_scene()
        
        if default_path and os.path.exists(default_path):
            logger.info(f"✓ Default themed scene generated: {default_path}")
        
        # Test custom themed prompts
        for prompt in custom_prompts:
            logger.info(f"\nTesting custom prompt: {prompt}")
            custom_path = generator.generate_themed_scene(theme_override=prompt)
            
            if custom_path and os.path.exists(custom_path):
                logger.info(f"✓ Custom themed scene generated: {custom_path}")
            
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_themed_scenes() 