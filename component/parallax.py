import pygame

class Parallax:
    def __init__(self, factor, ceil, floor=None):
        self.factor = factor
        self.ceil = ceil
        self.floor = floor
        self.offset = 0.0

    def offset_y_axis(self, target, layer):
        self.offset = (layer.rect.y + target.rect.y) * self.factor
        self.offset = min(self.offset, self.floor)
        self.offset = max(self.offset, self.ceil)
        layer.rect.y = self.offset