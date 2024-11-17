from src.generators.image_generator import ImageGenerator
from src.utils.logger import logger
from src.config.settings import SCENE_VARIATIONS
import os

def test_tavern_scenes():
    logger.info("=== Testing Tavern Study Room Scenes ===")
    
    try:
        generator = ImageGenerator()
        
        # Test base scene without variations
        logger.info("\nGenerating base tavern scene...")
        base_path = generator.generate_scene()
        
        if base_path and os.path.exists(base_path):
            logger.info(f"✓ Base scene generated: {base_path}")
        
        # Test one specific variation
        variation = "with rain droplets on the window panes"
        logger.info(f"\nGenerating scene with variation: {variation}")
        variation_path = generator.generate_scene(variation)
        
        if variation_path and os.path.exists(variation_path):
            logger.info(f"✓ Variation scene generated: {variation_path}")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_tavern_scenes() 