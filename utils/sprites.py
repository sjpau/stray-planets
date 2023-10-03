import pygame
from copy import deepcopy
from loader.loader import load_sprites

class SpriteStack:
    def __init__(self, path):
        self.images = load_sprites(path)
        self.sprites = {}

        for img in self.images:
            self.sprites[img] = [
                pygame.mask.from_surface(img),
                pygame.mask.from_surface(pygame.transform.flip(img, True, False)),
            ]
    
    def copy(self):
        return deepcopy(self.sprites)