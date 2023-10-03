import pygame
from defs.finals import SpriteIndex

class Entity(pygame.sprite.Sprite):
    def __init__(self, sprites: dict[pygame.Surface: [pygame.Mask, pygame.Mask]], group: pygame.sprite.Group, position: pygame.math.Vector2) -> None:
        super().__init__(group)
        self.group = group
        self.sprites = sprites
        try:
            self.image = next(iter(self.sprites.items()))[0]
        except IndexError:
            print('Entity sprite list is empty.')
        self.mask = self.sprites[self.image][SpriteIndex.MASK.value]
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    def update(self, dt):
        pass