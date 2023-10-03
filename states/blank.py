import pygame
from states.state import State
from entity.player import Player
from render.camera import Camera
from loader.assets import sprites_player

class StateBlank(State):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        img = pygame.Surface((16, 16))
        rct = img.get_rect()
        msk = pygame.mask.from_surface(img)
        self.sg_main = Camera(self.canvas)
        self.player = Player(sprites_player['idle'].sprites, self.sg_main, pygame.math.Vector2(0,0))
        self.sg_main.set_level_borders(0, 0, 0, 0)
    
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
    
    def update(self, dt):
        self.sg_main.attach_to(self.player)
        for sp in self.sg_main:
            sp.update(dt)

    def draw(self) -> pygame.Surface:
        self.canvas.fill((255, 255, 255))
        self.sg_main.render_all(self.canvas)
        return self.canvas