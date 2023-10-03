import pygame
from defs.finals import SpriteIndex

class Animation:
    def __init__(self, entity, sprites: dict[pygame.Surface: [pygame.Mask, pygame.Mask]], frame_duration: float):
        self.entity = entity
        self.sprites = sprites
        self.frame_duration = frame_duration
        self.flip = False
        self.frame_index = 0
        self.timer = 0

    def play(self, dt):
        self.timer += dt
        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            image, attributes = list(self.sprites.items())[self.frame_index]
            self.frame_index = (self.frame_index + 1) % len(self.sprites)
            if self.flip:
                self.entity.image = pygame.transform.flip(image, True, False)
                self.entity.mask = attributes[SpriteIndex.MASK_FLIPPED.value]
            else:
                self.entity.image = image
                self.entity.mask = attributes[SpriteIndex.MASK.value]

class AnimationHandler:
    def __init__(self, animations: dict[str: Animation]):
        self.animations = animations
        self._current = None
        self.play = True

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, name):
        if name in self.animations:
            if self._current != self.animations[name]:
                self._current = self.animations[name]
                self._current.timer = 0
                self._current.frame_index = 0

    def update(self, dt):
        if self.play:
            self.current.play(dt)