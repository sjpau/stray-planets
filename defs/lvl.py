import pygame
from defs.finals import PATH_FONT_LARGE, PATH_FONT_SMALL
from render.font import Font
from states.blank import StateBlank
from states.state import State

def get_states() -> { str: State }:
    states = {
        'blank': StateBlank(font_small=Font(PATH_FONT_LARGE), font_large=Font(PATH_FONT_SMALL))
        }
    return states

