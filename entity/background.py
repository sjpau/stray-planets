import pygame

from component.parallax import Parallax
from entity.entity import DeadEntity

class BackgroundLayer(DeadEntity):
    def __init__(self, *args, **kwargs):
        DeadEntity.__init__(self, args[0], args[1], args[2])
        self.parallax = Parallax(factor=kwargs.get('factor'), ceil=kwargs.get('ceil'), floor=kwargs.get('floor'))
        self.target = kwargs.get('target')

    def update(self, dt):
        if self.target is not None:
            self.parallax.offset_y_axis(self.target, self)