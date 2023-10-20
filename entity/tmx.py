import pygame
from entity.entity import Entity

# Classes that are required to read level from tmx data (all should be present when making tmx)
class Tile(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self.grid_position = kwargs.get('grid_position')
        self.climable = kwargs.get('climable')

class Decoration(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Spawner(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self._id = kwargs.get('_id')
        self.entity_spawn = kwargs.get('entity_spawn')
        self.active = kwargs.get('active')

    def spawn_entity(self, entity):
        if self.active:
            entity.rect.x = self.rect.x
            entity.rect.y = self.rect.y



class Trigger(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self._id = kwargs.get('_id')
        self._type = kwargs.get('_type')
        self.action = kwargs.get('action')
        self.desired_receiver_id = kwargs.get('desired_receiver_id')


class Wall(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self.climable = kwargs.get('climable')

class Limit(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Spike(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])

class Pickup(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self.active = kwargs.get('active')
        self.ability = kwargs.get('ability')

class TextObject(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self.text = kwargs.get('text')
        self.font = kwargs.get('font')
        self.font.change_color(kwargs.get('color'))