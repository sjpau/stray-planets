from typing import Final
from enum import Enum
import pygame

tile_size: Final = 16

display_resolution: Final = {
    '640x360': (640, 360),
    '1280x720': (1280, 720),
    '1920x1080': (1920, 1080),
}

CANVAS_WIDTH: Final = 320
CANVAS_HEIGHT: Final = 180

CAPTION: Final = "Stray planets"

PATH_FONT_LARGE = 'data/assets/png/font/large_font.png'
PATH_FONT_SMALL = 'data/assets/png/font/small_font.png'

COLOR_BLACK: Final = pygame.Color((16, 13, 19))
COLOR_WHITE: Final = pygame.Color((255, 255, 255))
COLOR_HERO_SLIDE_MAIN: Final = pygame.Color((255, 255, 255))
COLOR_HERO_SLIDE_SUB: Final = pygame.Color((183, 198, 217))
COLOR_HERO_SLIDE_EYES: Final = pygame.Color((6, 6, 47))

class SpriteIndex(Enum):
    MASK            = 0
    MASK_FLIPPED    = 1