"""
Prompt Library - Cozy Cafe Study Scenes
Successfully tested and verified for consistent, high-quality output.
Last updated: 2024-11-16
"""

# Refined base prompt with stronger instructions
VERIFIED_BASE_PROMPT = """
Create only a single scene image without any additional elements, NO color palettes, and NO text overlays!: 
A cozy cafe corner that feels like a warm hug. 
The scene focuses on an intimate window nook with deep cushions and soft throw blankets. 
Warm brick or wood-paneled walls create a rich, textural backdrop. 
Edison bulb pendant lights cast a golden glow, mixing with soft natural light from large windows. 
A rustic wooden table holds a steaming latte in a ceramic mug. 
Plush cushions, knit textures, and subtle decor create an inviting study space.
The atmosphere should feel incredibly warm, peaceful, and embracing.
Generate this scene only, with no additional visual elements or information in the frame.
""".strip()

# Verified working variations
VERIFIED_VARIATIONS = [
    "during golden hour with warm sunlight making everything glow",
    "on a misty morning with diffused golden light streaming in",
    "during blue hour with warm interior lights contrasting the dusky sky",
    "with soft morning light creating gentle shadows",
    "at dusk with cozy interior lighting"
]

# Style guidance with explicit instructions
VERIFIED_STYLE_GUIDANCE = """
Create a single photo-realistic scene. Do not include any color palettes, text, or additional information.
Use a rich, warm color palette with deep browns, warm golds, soft creams, and touches of terracotta. 
The lighting should feel golden and embracing, creating a cocoon-like atmosphere. 
Focus on layered textures: worn wood, soft fabrics, smooth ceramics, and organic elements. 
Generate only the scene itself, nothing else in the frame.
""".strip()

# Generation settings that produced good results
VERIFIED_SETTINGS = {
    'image_size': "1792x1024",
    'quality': "hd",
    'style': "natural",
    'target_resolution': (1920, 1080),
    'fps': 30,
    'duration': 3600  # 1 hour in seconds
} 