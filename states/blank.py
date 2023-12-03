import pygame
from states.state import State
import defs.finals as finals
import debug 
from entity.player import Player
from render.camera import Camera
import loader.mapper as mapper
from loader.loader import png
import random
from math import pi
from loader.assets import sprites_player
from loader.assets import sprites_env_dust
from component.animation import Animation
from loader.loader import load_sprites
from loader.assets import sprites_background_layers
from utils.utils import bool_dict_set_true
from entity.background import BackgroundLayer
from entity.shadow import ShadowSprite
from entity.particles import ParticleSpark, ParticleAnimated

class StateBlank(State):
    def __init__(self, tmx_maps, map_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tmx_maps = tmx_maps
        self.map_key = map_key
        self.background = png('data/assets/png/background/sodium/background.png')
        self.sg_camera = Camera(self.canvas)
        self.sg_tiles_colliders = Camera(self.canvas)
        self.sg_tiles_spikes = Camera(self.canvas)
        self.sg_tiles_non_colliders = Camera(self.canvas)
        self.sg_decor_fg = Camera(self.canvas)
        self.sg_decor_bg = Camera(self.canvas)
        self.sg_dust_fg = Camera(self.canvas)
        self.sg_dust_bg = Camera(self.canvas)
        self.sg_triggers = Camera(self.canvas)
        self.sg_spawners = Camera(self.canvas)
        self.sg_limits = Camera(self.canvas)
        self.sg_enemies = Camera(self.canvas)
        self.sg_attack_hitboxes = Camera(self.canvas)
        self.sg_shadow_sprites = Camera(self.canvas)
        self.sg_background_layers = Camera(self.canvas)
        self.sg_clouds = Camera(self.canvas)
        self.sg_walls = Camera(self.canvas)
        self.sg_walls_enemy = Camera(self.canvas)
        self.sg_spikes = Camera(self.canvas)
        self.sg_pickups = Camera(self.canvas)
        self.sg_text_objects = Camera(self.canvas)
        self.sg_camera_groups = [self.sg_tiles_colliders, self.sg_tiles_non_colliders,
                                 self.sg_decor_fg, self.sg_decor_bg,
                                 self.sg_camera, self.sg_triggers,
                                 self.sg_spawners, self.sg_attack_hitboxes,
                                 self.sg_shadow_sprites, self.sg_limits,
                                 self.sg_enemies, self.sg_background_layers,
                                 self.sg_clouds, self.sg_walls_enemy,
                                 self.sg_tiles_spikes, self.sg_spikes,
                                 self.sg_pickups, self.sg_text_objects,
                                 self.sg_walls, self.sg_dust_bg,
                                 self.sg_dust_fg,
                                 ]
        self.tmx_tile_layers_to_sg = {
            'colliders': self.sg_tiles_colliders,
            'spikes': self.sg_tiles_spikes,
            'background': self.sg_tiles_non_colliders,
        }
        self.tmx_obj_layers_to_sg = {
            'decor_fg': self.sg_decor_fg,
            'decor_bg': self.sg_decor_bg,
            'triggers': self.sg_triggers,
            'spawners': self.sg_spawners,
            'camera_limits': self.sg_limits,
            'walls_invisible': self.sg_walls,
            'walls_invisible_enemy': self.sg_walls_enemy,
            'spike_colliders': self.sg_spikes,
            'pickups': self.sg_pickups,
            'text': self.sg_text_objects,
        }
        self.player_shadow_cd = 40
        self.player_shadow_count = 0
        self.player = None
        self.particles_dust = []
        self.particles_sparks = []
        self.player_box = None
        self.player_persistent_data = None
        self.desired_next_state = ""
        self.transition = -30
        self.transition_start = False

    def on_exit(self):
        pass

    def preload(self, player_persistent_data=None):
        # Clean up
        self.player_shadow_cd = 40
        self.player_shadow_count = 0
        self.player = None
        self.particles_dust = []
        self.particles_sparks = []
        self.player_box = None
        self.player_persistent_data = player_persistent_data
        self.desired_next_state = ""
        self.transition = -30
        self.transition_start = False
        for group in self.sg_camera_groups:
            group.empty()
        # Load map data
        _, _, _, _, _, _, _, _, _, _ = mapper.unpack_tmx(self.tmx_maps, self.map_key, 
                                    self.tmx_tile_layers_to_sg, 
                                    self.tmx_obj_layers_to_sg)
        # Managing entities
        self.player = Player(sprites_player['idle'].sprites, self.sg_camera, pygame.math.Vector2(0,0))
        self.player_box = pygame.FRect(self.canvas.get_rect())
        for spawner in self.sg_spawners:
            if spawner.entity_spawn == 'player': # TODO check for id in persistence variable
                spawner.spawn_entity(self.player)

        # Calculate level borders
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for tile in self.sg_limits:
            x, y, width, height = tile.rect
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x + width > max_x:
                max_x = x + width
            if min_y is None or y < min_y:
                min_y = y
            if max_y is None or y + height > max_y:
                max_y = y + height
        for camera in self.sg_camera_groups:
            camera.set_level_borders(min_x, min_y, max_x, max_y)

        factor = 0.001        
        for img in sprites_background_layers:
            factor += 0.005
            BackgroundLayer(img, self.sg_background_layers, pygame.math.Vector2(0, 0), floor=5, ceil=-5, factor=factor, target=self.player)

        self.ready = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.VIDEORESIZE:
            self.on_videoresize()
        if self.handle['player input']:
            self.player.handle_input(event)

    def update(self, dt):
        for group in self.sg_camera_groups:
            group.update(dt)
            group.attach_to(self.player)
        for spark in self.particles_sparks:
            spark.update(dt)
        for spark in self.particles_sparks:
            if spark.kill:
                self.particles_sparks.remove(spark) # TODO removing during iteration

        self.player.entity_movement_collision_horizontal([self.sg_tiles_colliders, self.sg_walls])
        self.player.entity_movement_collision_vertical([self.sg_tiles_colliders, self.sg_walls])

        for hit in pygame.sprite.spritecollide(self.player, self.sg_triggers, False):
            if hit.action == 'teleport' and hit._type == 'sender':
                find_id = hit.desired_receiver_id
                for trigger in self.sg_triggers:
                    if int(find_id) == int(trigger.t_id):
                        self.player.rect.topleft = trigger.rect.topleft
                        break
            if hit.action == 'transist':
                self.player_persistent_data.spawner_id = hit.desired_receiver_id
                self.desired_next_state = hit.action_receiver
        self.player_box.center = self.player.rect.center
        # Cool dashing animation
        if self.player.body.in_dash:
            ShadowSprite(self.sg_shadow_sprites, color=finals.COLOR_WHITE, target=self.player, alpha_dec=15)
            dir_key = [key for key, value in self.player.direction.items() if value]
            self.particles_sparks.append(ParticleSpark(pygame.math.Vector2(self.player.rect.center), finals.COLOR_WHITE, random.random() - 0.5 + pi * self.player.direction_pi[dir_key[0]], 2 + random.random()))
        for s in self.sg_shadow_sprites:
            if s.kill == True:
                self.sg_shadow_sprites.remove(s)
        # Dust particle generation
        dust_pos = pygame.math.Vector2(random.randint(int(self.player_box.x), int(self.player_box.x + self.player_box.width)),  
                                        random.randint(int(self.player_box.y), int(self.player_box.y + self.player_box.height)))
        if random.random() < 0.01:
            surf =  pygame.Surface((4,4))
            surf.set_colorkey((0,0,0))
            self.particles_dust.append(ParticleAnimated(sprites_env_dust['dust'].sprites, self.sg_dust_bg, dust_pos)) if random.random() < 0.5 else self.particles_dust.append(ParticleAnimated(sprites_env_dust['dust'].sprites, self.sg_dust_fg, dust_pos))
        for p in self.particles_dust:
            if p.kill:
                self.particles_dust.remove(p)
                p.group.remove(p)
        
        if self.desired_next_state != '':
            self.transition_start = True
        if self.transition_start:
            self.transition += 1
            if self.transition > 30:
                self.done = True
        if self.transition < 0:
            self.transition += 1

    def draw(self):
        self.canvas.blit(self.background, (0,0))
        for sprite in self.sg_background_layers.sprites():
            self.canvas.blit(sprite.image, sprite.rect.topleft)
        self.sg_clouds.render_all_parallax(self.canvas)
        self.sg_dust_bg.render_all(self.canvas)
        self.sg_decor_bg.render_all(self.canvas)
        self.sg_tiles_non_colliders.render_all(self.canvas)
        self.sg_tiles_colliders.render_all(self.canvas)
        self.sg_spikes.render_all(self.canvas)
        self.sg_tiles_spikes.render_all(self.canvas)
        self.sg_shadow_sprites.render_all(self.canvas)
        self.sg_camera.render_all(self.canvas)
        self.sg_decor_fg.render_all(self.canvas)
        self.sg_dust_fg.render_all(self.canvas)
        self.sg_limits.render_all(self.canvas)
        self.sg_enemies.render_all(self.canvas)
        self.sg_attack_hitboxes.render_all(self.canvas)
        self.sg_walls_enemy.render_all(self.canvas)
        self.sg_spikes.render_all(self.canvas)
        self.sg_pickups.render_all(self.canvas)
        self.sg_text_objects.render_all(self.canvas)
        for obj in self.sg_text_objects:
            obj.font.render(obj.image, obj.text, (obj.image.get_width()/2, obj.image.get_height()/2), center=True)
        for spark in self.particles_sparks:
            spark.draw(self.canvas, self.sg_camera)

        if self.transition:
            t_surf = pygame.Surface(self.canvas.get_size())
            pygame.draw.circle(t_surf, finals.COLOR_WHITE, (finals.CANVAS_WIDTH//2, finals.CANVAS_HEIGHT//2), (30 - abs(self.transition)) * 8)
            t_surf.set_colorkey(finals.COLOR_WHITE)
            self.canvas.blit(t_surf, (0, 0))

        return self.canvas