import pygame
from defs.finals import SpriteIndex

class Animation:
    def __init__(self, sprites: dict[pygame.Surface: [pygame.Mask, pygame.Mask]], frame_duration: float):
        self.sprites = sprites
        self.frame_duration = frame_duration
        self.flip = False
        self.frame_index = 0
        self.timer = 0
        self.current_image, attrs = list(self.sprites.items())[self.frame_index]
        self.current_mask = attrs[SpriteIndex.MASK.value]

    def play(self, dt):
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            image, attributes = list(self.sprites.items())[self.frame_index]
            self.frame_index = (self.frame_index + 1) % len(self.sprites)
            if self.flip:
                self.current_mask = attributes[SpriteIndex.MASK_FLIPPED.value]
            else:
                self.current_mask = attributes[SpriteIndex.MASK.value]
            self.current_image = image

class AnimationHandler:
    def __init__(self, entity, animations: dict[str: Animation]):
        self.entity = entity
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
            if self.current.flip:
                self.entity.image = pygame.transform.flip(self.current.current_image, True, False)
            else:
                self.entity.image = self.current.current_image
            self.entity.mask = self.current.current_mask