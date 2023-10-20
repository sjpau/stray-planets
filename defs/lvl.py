import pygame
from defs.finals import PATH_FONT_LARGE, PATH_FONT_SMALL
from render.font import Font
from states.blank import StateBlank
from states.state import State
from pytmx import load_pygame

def get_states() -> { str: State }:
    tmx_maps = {
        'sodium_one': load_pygame('data/assets/tmx/sodium/sodium_1.tmx'),
    }

    states = {
        'blank': StateBlank(tmx_maps, 'sodium_one', font_small=Font(PATH_FONT_LARGE), font_large=Font(PATH_FONT_SMALL))
        }
    return states

