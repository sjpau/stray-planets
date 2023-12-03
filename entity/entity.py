import pygame
from defs.finals import SpriteIndex

class DeadEntity(pygame.sprite.Sprite):
    def __init__(self, image: pygame.image, group: pygame.sprite.Group, position: pygame.math.Vector2):
        super().__init__(group)
        self.group = group
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    def update(self, dt):
        pass

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
        self.rect = self.image.get_frect()
        self.rect.topleft = position
        self.direction = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.direction_pi = {
            "left": 1,
            "right": 0,
            "up": 1.5,
            "down": 0.5,
        }

    def entity_movement_collision_horizontal(self, collide_groups):
        self.body.movement_horizontal() # Entity must have Body component for collision
        for group in collide_groups:
            for hit in pygame.sprite.spritecollide(self, group, False):
                if self.body.velocity.x < 0:
                    self.rect.left = hit.rect.right
                if self.body.velocity.x > 0:
                    self.rect.right = hit.rect.left
                if not self.body.on_ground and self.state['slide'] and hit.climable:
                    self.body.velocity.y = min(self.body.velocity.y, 0.3)
                    self.body.jumps = 1

    def entity_movement_collision_vertical(self, collide_groups):
        self.body.movement_vertical() # Entity must have Body component for collision
        for group in collide_groups:
            for hit in pygame.sprite.spritecollide(self, group, False):
                if self.body.velocity.y > 0:
                    self.rect.bottom = hit.rect.top
                    self.body.velocity.y = 0
                    self.body.jumps = 2
                if self.body.velocity.y < 0:
                    self.rect.top = hit.rect.bottom 
                    self.body.velocity.y = 0   

    def update(self, dt):
        pass