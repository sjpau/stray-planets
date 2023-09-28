import pygame
from states.state import State

class StateBlank(State):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
    
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
    
    def update(self, dt):
        pass

    def draw(self) -> pygame.Surface:
        self.canvas.fill((255, 255, 255))
        return self.canvas