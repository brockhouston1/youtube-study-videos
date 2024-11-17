from openai import OpenAI
import requests
from pathlib import Path
from datetime import datetime
import random
from PIL import Image
import io

from src.utils.logger import logger
from src.config.settings import (
    OPENAI_API_KEY,
    IMAGES_DIR,
    IMAGE_SIZE,
    IMAGE_QUALITY,
    IMAGE_STYLE,
    VIDEO_RESOLUTION,
    BASE_PROMPT,
    SCENE_VARIATIONS,
    STYLE_GUIDANCE
)

class ImageGenerator:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set in environment variables")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.images_dir = IMAGES_DIR
        self.images_dir.mkdir(exist_ok=True)

    def generate_scene(self, variation=None):
        """Generate a consistent tavern study scene with optional variation"""
        try:
            # Start with base prompt
            prompt = BASE_PROMPT
            
            # Add variation if specified
            if variation:
                prompt += f" {variation}"
            elif random.random() > 0.3:  # 70% chance to add random variation
                prompt += f" {random.choice(SCENE_VARIATIONS)}"
            
            # Add style guidance
            prompt += f" {STYLE_GUIDANCE}"
            
            logger.info(f"Generating scene with prompt: {prompt}")

            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=IMAGE_SIZE,
                quality=IMAGE_QUALITY,
                style=IMAGE_STYLE,
                n=1
            )

            image_url = response.data[0].url
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_path = self.images_dir / f"tavern_study_{timestamp}.png"
            
            # Download and save the image
            final_path = self.download_and_process_image(image_url, image_path)
            logger.info(f"✓ Scene generated successfully: {final_path}")
            return final_path

        except Exception as e:
            logger.error(f"Failed to generate scene: {str(e)}")
            return None

    def download_and_process_image(self, url, save_path):
        """Download image and process it to match video requirements"""
        try:
            # Download the image
            response = requests.get(url)
            response.raise_for_status()
            
            # Load image into PIL
            image = Image.open(io.BytesIO(response.content))
            
            # Resize to match video resolution if needed
            if image.size != VIDEO_RESOLUTION:
                logger.info(f"Resizing image from {image.size} to {VIDEO_RESOLUTION}")
                image = image.resize(VIDEO_RESOLUTION, Image.Resampling.LANCZOS)
            
            # Save processed image
            image.save(save_path, 'PNG', quality=95)
            logger.debug(f"Processed image saved to: {save_path}")
            
            return save_path
            
        except Exception as e:
            logger.error(f"Failed to process image: {str(e)}")
            return None

    def enhance_prompt(self, base_prompt):
        """Enhance the prompt with fantasy/medieval-specific details"""
        # Select a subset of enhancements to avoid making prompt too long
        selected_enhancements = random.sample(PROMPT_ENHANCEMENTS, 4)
        style_guide = random.choice(STYLE_GUIDANCE)
        
        # Build the enhanced prompt
        enhanced_prompt = f"""
        {base_prompt}. 
        The scene should be highly detailed and perfect for a lofi study video background.
        {', '.join(selected_enhancements)}.
        {style_guide}.
        Ensure the scene has elements that could be subtly animated, like floating magical particles,
        gentle candlelight, or softly swirling potion steam.
        The overall mood should be cozy, peaceful, and conducive to studying.
        """.strip()
        
        logger.debug(f"Enhanced prompt: {enhanced_prompt}")
        return enhanced_prompt

    def generate_themed_scene(self, theme_override=None):
        """Generate a scene with specific theme focus"""
        try:
            base_prompt = theme_override or random.choice(SCENE_PROMPTS)
            
            # Add specific theme elements
            theme_elements = [
                "medieval fantasy aesthetic",
                "magical study atmosphere",
                "cozy fantasy cafe setting",
                "detailed background art style"
            ]
            
            theme_prompt = f"{base_prompt} {', '.join(theme_elements)}"
            return self.generate_scene(custom_prompt=theme_prompt)
            
        except Exception as e:
            logger.error(f"Failed to generate themed scene: {str(e)}")
            return None