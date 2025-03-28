"""
settings.py

Global configuration settings for the Snake game project.
"""

# Display settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 800
FPS: int = 15

# Colors (fallback if images not used)
COLOR_BACKGROUND: tuple[int, int, int] = (0, 0, 0)
COLOR_SNAKE: tuple[int, int, int] = (0, 255, 0)
COLOR_FOOD: tuple[int, int, int] = (255, 0, 0)

# Speed settings
SNAKE_SPEED: int = 15
FOOD_RESPAWN_TIME: float = 5.0
INITIAL_SNAKE_LENGTH: int = 5
BLOCK_SIZE = 40

MUSIC_VOLUME: float = 0.6

# Asset paths
BACKGROUND_IMAGE_PATH: str = "assets/images/background.jpg"
SNAKE_FONT_PATH: str = "assets/fonts/snake-game.ttf"

# Dictionary for snake images
SNAKE_IMAGES = {
    "head_up": "assets/images/head_up.png",
    "head_down": "assets/images/head_down.png",
    "head_left": "assets/images/head_left.png",
    "head_right": "assets/images/head_right.png",

    "body_vertical": "assets/images/body_vertical.png",
    "body_horizontal": "assets/images/body_horizontal.png",
    "body_topleft": "assets/images/body_topleft.png",
    "body_topright": "assets/images/body_topright.png",
    "body_bottomleft": "assets/images/body_bottomleft.png",
    "body_bottomright": "assets/images/body_bottomright.png",

    "tail_up": "assets/images/tail_up.png",
    "tail_down": "assets/images/tail_down.png",
    "tail_left": "assets/images/tail_left.png",
    "tail_right": "assets/images/tail_right.png",
}

# Apple image path
APPLE_IMAGE_PATH = "assets/images/apple.png"

# Audio paths
SOUND_FOOD: str = "assets/audio/food.mp3"
SOUND_GAMEOVER: str = "assets/audio/gameover.mp3"
SOUND_MOVE: str = "assets/audio/move.mp3"
MUSIC_BACKGROUND: str = "assets/audio/music.mp3"

# --- Additional configuration for user customization ---
# Path to configuration file
CONFIG_FILE_PATH: str = "config/config.json"

# User adjustable settings (defaults)
BACKGROUND_MUSIC: bool = True       # True = on, False = off
DIFFICULTY: str = "easy"             # Options: "easy", "medium", "hard"
THEME: str = "default"               # Options: "default", "modern"
