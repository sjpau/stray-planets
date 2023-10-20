import pygame
from entity.entity import DeadEntity

class ShadowSprite(DeadEntity):
    def __init__(self, *args, **kwargs):
        self.target = kwargs.get('target')
        self.position = pygame.math.Vector2(self.target.rect.topleft)
        self.mask = pygame.mask.from_surface(self.target.image)
        self.image = self.mask.to_surface()
        self.image.set_colorkey((0,0,0))
        w, h = self.image.get_size()
        self.color = kwargs.get('color')
        DeadEntity.__init__(self, self.image, args[0], self.position)
        for x in range(w):
            for y in range(h):
                if self.image.get_at((x,y))[0] != 0:
                    self.image.set_at((x,y), self.color)
        self.alpha = 255
        self.alpha_dec = kwargs.get('alpha_dec')
        self.kill = False
    
    def update(self, dt):
        self.alpha -= self.alpha_dec
        self.image.set_alpha(self.alpha)
        if self.alpha == 0:
            self.kill = True
