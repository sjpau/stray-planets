import pygame
from entity.entity import Entity
from component.body import Body
from component.animation import AnimationHandler, Animation
from loader.assets import sprites_player

class Player(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self.body = Body(self.rect)
        self.animation_handler = AnimationHandler(
            {
            'idle': Animation(self, sprites_player['idle'].sprites, 200),
            }
        )
        self.animation_handler.play = True
        self.animation_handler.current = 'idle'
    
    def update(self, dt):
        self.animation_handler.update(dt)