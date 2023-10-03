import pygame
from entity.entity import Entity

# Classes that are required to read level from tmx data (all should be included when making tmx)
# TODO: implement all
class Tile(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self.grid_position = grid_position
        self.climable = climable

class Decoration(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Spawner(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Trigger(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Wall(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Limit(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Spike(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Pickup(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class TextObject(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])