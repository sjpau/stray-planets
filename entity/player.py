import pygame
from entity.entity import Entity
from component.body import Body
from component.animation import AnimationHandler, Animation
from loader.assets import sprites_player
from utils.utils import bool_dict_set_true

class Player(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, args[0], args[1], args[2])
        self.body = Body(self.rect)
        self.animation_handler = AnimationHandler(self,
            {
            'idle': Animation(sprites_player['idle'].sprites, 200),
            }
        )
        self.animation_handler.play = True
        self.animation_handler.current = 'idle'

        self.want_move = {
            'right': False,
            'left': False,
        }
        # TODO: implement state switching menu/bar
        self.state = {
            'slide': True,
            'dash': True,
            'combat': True,
        }
        self.keys_right = {pygame.K_RIGHT, pygame.K_l, pygame.K_d}
        self.keys_left = {pygame.K_LEFT, pygame.K_h, pygame.K_a}
        self.keys_up = {pygame.K_UP, pygame.K_k, pygame.K_w}
        self.keys_down = {pygame.K_DOWN, pygame.K_j, pygame.K_s}
        self.keys_jump = {pygame.K_SPACE}
        self.keys_dash = {pygame.K_LSHIFT}

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            k = event.key
            if k in self.keys_right:
                self.want_move['right'] = True
                bool_dict_set_true(self.direction, 'right')
            elif k in self.keys_left:
                self.want_move['left'] = True
                bool_dict_set_true(self.direction, 'left')
            elif k in self.keys_dash:
                if self.state['dash']:
                    self.body.dash(self.direction)
            elif k in self.keys_jump:
                self.body.jump()
        if event.type == pygame.KEYUP:
            k = event.key
            if k in self.keys_right:
                self.want_move['right'] = False
            elif k in self.keys_left:
                self.want_move['left'] = False
    
    def switch_state(self, state_name: str) -> None:
        bool_dict_set_true(self.state, state_name)
        #TODO switch color palette
        #TODO spark particles

    def update(self, dt):
        if self.want_move['right']:
            self.body.velocity.x = 1
        if self.want_move['left']:
            self.body.velocity.x = -1
        if not self.want_move['right'] and not self.want_move['left']:
            self.body.velocity.x = 0
        if self.direction['left']:
            self.animation_handler.current.flip = True
        if self.direction['right']:
            self.animation_handler.current.flip = False
        self.body.dash_update()
        self.animation_handler.update(dt)