from pathlib import Path
import os
from dotenv import load_dotenv
from src.config.prompt_library import (
    VERIFIED_BASE_PROMPT as BASE_PROMPT,
    VERIFIED_VARIATIONS as SCENE_VARIATIONS,
    VERIFIED_STYLE_GUIDANCE as STYLE_GUIDANCE,
    VERIFIED_SETTINGS
)

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Media Paths
IMAGES_DIR = ASSETS_DIR / "images"
ANIMATIONS_DIR = ASSETS_DIR / "animations"
MUSIC_DIR = ASSETS_DIR / "music"

# Create necessary directories
for directory in [ASSETS_DIR, OUTPUT_DIR, LOGS_DIR, IMAGES_DIR, ANIMATIONS_DIR, MUSIC_DIR]:
    directory.mkdir(exist_ok=True)

# Image Generation Settings
IMAGE_SIZE = VERIFIED_SETTINGS['image_size']
IMAGE_QUALITY = VERIFIED_SETTINGS['quality']
IMAGE_STYLE = VERIFIED_SETTINGS['style']

# Video Settings
VIDEO_RESOLUTION = (1920, 1080)
VIDEO_FPS = 30
VIDEO_DURATION = 3600  # 1 hour in seconds
BASE_VIDEO_DURATION = 5  # Duration of the base loopable video in seconds

# Scene Prompts for Medieval/Fantasy Cafe Settings
SCENE_PROMPTS = [
    "Rustic medieval tavern interior with exposed wooden beams, warm candlelight, and a stone fireplace",
    "Historic stone-walled cafe with leaded glass windows, iron lanterns, and steaming coffee cups on wooden tables",
    "Ancient library cafe with tall oak bookshelves, leather-bound books, and scholars quietly studying at antique desks",
    "Traditional coffee house with timber-framed architecture, copper brewing equipment, and servers in period dress",
    "Medieval marketplace cafe with cast iron cookware, dried herbs hanging from rafters, and fresh baked goods on display",
    "Cozy cellar cafe with vaulted stone ceilings, wrought iron candelabras, and intimate seating nooks",
    "Converted monastery cafe with gothic arched windows, weathered wooden tables, and morning light streaming in",
    "Historic underground coffee hall with rough stone walls, iron-bound wooden furniture, and warm ambient lighting"
]

# Prompt Enhancements for better results
PROMPT_ENHANCEMENTS = [
    "high quality",
    "detailed realistic art style",
    "magical aesthetic",
    "perfect for lofi study video background",
    "seamless loop potential",
    "subtle animation-ready magical elements",
    "inspired by Studio Ghibli's detailed backgrounds",
    "rich textures and atmospheric lighting"
]

# Debug Settings
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Verify critical files exist
def verify_settings():
    from src.utils.logger import logger
    
    # Check client_secrets.json
    if not CLIENT_SECRETS_FILE.exists():
        logger.error(f"❌ client_secrets.json not found at {CLIENT_SECRETS_FILE}")
        raise FileNotFoundError("client_secrets.json is required for YouTube API authentication")
    
    logger.info("✓ Settings loaded successfully")
    if DEBUG:
        logger.debug(f"Base Directory: {BASE_DIR}")
        logger.debug(f"Assets Directory: {ASSETS_DIR}")
        logger.debug(f"Output Directory: {OUTPUT_DIR}") 