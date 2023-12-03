import pygame

class Body:
    def __init__(self, _rect: pygame.FRect, speed=1.25, gravity=0.1, jump_speed=-2.8, jumps=1, dash_cd=100, dash_dist=20):
        self._rect = _rect
        self.direction = {
            'left': False,
            'right': False,
            'up': False,
            'down': False,
        }
        self.speed = speed
        self.velocity = pygame.math.Vector2(0,0)
        self.on_ground = False
        self.gravity = gravity
        self.jump_speed = jump_speed
        self.jumps = jumps
        self.dashing = 0
        self.dash_cd = dash_cd
        self.in_dash = False
        self.dash_dist = dash_dist

    def apply_gravity(self):
        self.velocity.y += self.gravity
        self._rect.y +=  self.velocity.y

    def jump(self):
        if self.jumps > 0:
            self.velocity.y = self.jump_speed
            self.jumps -= 1
    
    def dash(self, direction):
        if not self.dashing:
            if self.direction['right']:
                self.dashing = self.dash_cd + self.dash_dist
            if self.direction['left']:
                self.dashing = -self.dash_cd - self.dash_dist

    def movement_horizontal(self):
        self._rect.x += self.velocity.x * self.speed
        if self.velocity.x < 0:
            self.direction['left'] = True
            self.direction['right'] = False
        elif self.velocity.x > 0:
            self.direction['right'] = True
            self.direction['left'] = False
    
    def movement_vertical(self):
        self.apply_gravity()
        if self.velocity.y > self.gravity or self.velocity.y < -self.gravity:
            self.on_ground = False
        else:
            self.on_ground = True
    
    def dash_update(self):
        self.in_dash = False
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > self.dash_cd:
            self.in_dash = True
            self.velocity.x = abs(self.dashing) / self.dashing * 3
            if self.dashing == self.dash_cd + 1:
                self.velocity.x *= 0.1
        
        if self.velocity.x > 0:
            self.velocity.x = max(self.velocity.x - 0.1, 0)
        else:
            self.velocity.x = min(self.velocity.x + 0.1, 0)