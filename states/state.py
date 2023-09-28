import pygame
import defs.finals as finals
from loader.save import PersistentData


class State(object):
    def __init__(self, font_small=None, font_large=None, desired_next_state="", name="", state_persistent_data=PersistentData()):
        self.done = False
        self.quit = False
        self.font_small = font_small
        self.font_large = font_large
        self.next_state = None
        self.name = name
        self.desired_next_state = desired_next_state
        self.state_persistent_data = state_persistent_data
        self.persist = {}
        self.canvas = pygame.Surface((finals.CANVAS_WIDTH, finals.CANVAS_HEIGHT))
        self.canvas_rect = self.canvas.get_rect()
        self.handle = {
            'player input': True,
            'level update': True,
            'level draw': True,
        }
        self.ready = False
        self.fullscreen = False

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def manage_music(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def preload(self):
        pass

    def update(self, dt):
        pass

    def draw(self) -> pygame.Surface:
        pass
