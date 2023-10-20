import pygame
import pytmx
from entity.tmx import Decoration, Spawner, Trigger, Limit, Wall, Spike, Pickup, TextObject, Tile
from defs.finals import tile_size
from loader.loader import png
from render.font import Font
from utils.utils import image_to_sprite_dict

def unpack_tmx(tmx_data, lvl_name, tile_layers_to_groups, obj_layers_to_groups):
    tmx_tiles = []
    tmx_decor = []
    tmx_triggers = []
    tmx_spawners = []
    tmx_limits = []
    tmx_walls = []
    tmx_enemy_walls = []
    tmx_spikes = []
    tmx_pickups = []
    tmx_text = []
    # Tiles
    for layer in tmx_data[lvl_name].visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                grid_pos = (x,y)
                pos = pygame.math.Vector2(x * tile_size, y * tile_size)
                surf = image_to_sprite_dict(surf)
                t = Tile(surf, tile_layers_to_groups[layer.name], pos, grid_position=grid_pos, climable=True)
                tmx_tiles.append(t)
    # Objects
    for obj_layer_name in obj_layers_to_groups.keys():
        layer = tmx_data[lvl_name].get_layer_by_name(obj_layer_name)
        for obj in layer:
            if obj.type == 'Static':
                pos = pygame.math.Vector2(obj.x, obj.y)
                sprites = image_to_sprite_dict(obj.image)
                d = Decoration(sprites, obj_layers_to_groups[obj_layer_name], pos)
                tmx_decor.append(d)
            if obj.type == 'Trigger':
                pos = pygame.math.Vector2(obj.x, obj.y)
                s = pygame.Surface((int(obj.width), int(obj.height)))
                s.set_alpha(0)
                surf = image_to_sprite_dict(s)
                _id = obj.id
                _type = obj.t_type
                action = obj.action
                if _type == "sender":
                    desired_receiver_id = obj.desired_receiver_id
                else:
                    desired_receiver_id = ""
                t = Trigger(surf, obj_layers_to_groups[obj_layer_name], pos, _type=_type, _id=_id, desired_receiver_id=desired_receiver_id, action=action)
                tmx_triggers.append(t)
            if obj.type == 'Transitioner':
                pos = pygame.math.Vector2(obj.x, obj.y)
                s = pygame.Surface((int(obj.width), int(obj.height)))
                s.set_alpha(0)
                surf = image_to_sprite_dict(s)
                _id = obj.id
                _type = obj.t_type
                if _type == "sender":
                    desired_receiver_id = obj.desired_receiver_id
                else:
                    desired_receiver_id = ""
                action = obj.action
                transition_to = obj.transition_to_class
                t = Trigger(surf, obj_layers_to_groups[obj_layer_name], pos, _type=_type, _id=_id, desired_receiver_id=desired_receiver_id, action=action, action_receiver=transition_to)
            if obj.type == 'Spawner':
                pos = pygame.math.Vector2(obj.x, obj.y)
                s = pygame.Surface((int(obj.width), int(obj.height)))
                s.set_alpha(0)
                surf = image_to_sprite_dict(s)
                entity_spawn = obj.entity
                active = obj.active
                _id = obj.id
                s = Spawner(surf, obj_layers_to_groups[obj_layer_name], pos, entity_spawn=entity_spawn, active=active, _id=_id)
                tmx_spawners.append(s)
            if obj.type == 'Limit':
                pos = pygame.math.Vector2(obj.x, obj.y)
                s = pygame.Surface((int(obj.width), int(obj.height)))
                s.set_alpha(0)
                surf = image_to_sprite_dict(s)
                l = Limit(surf, obj_layers_to_groups[obj_layer_name], pos, obj.limit_on)
                tmx_limits.append(l)
            if obj.type == 'Wall':
                pos = pygame.math.Vector2(obj.x, obj.y)
                s = pygame.Surface((int(obj.width), int(obj.height)))
                s.set_alpha(0)
                surf = image_to_sprite_dict(s)
                w = Wall(surf, obj_layers_to_groups[obj_layer_name], pos)
                tmx_walls.append(w)
            if obj.type == 'WallForEnemy':
                pos = pygame.math.Vector2(obj.x, obj.y)
                s = pygame.Surface((int(obj.width), int(obj.height)))
                s.set_alpha(0)
                surf = image_to_sprite_dict(s)
                w = Wall(surf, obj_layers_to_groups[obj_layer_name], pos)
                tmx_enemy_walls.append(w)
            if obj.type == 'Spike':
                pos = pygame.math.Vector2(obj.x, obj.y)
                s = pygame.Surface((int(obj.width), int(obj.height)))
                s.set_alpha(0)
                surf = image_to_sprite_dict(s)
                s = Spike(surf, obj_layers_to_groups[obj_layer_name], pos)
                tmx_spikes.append(s)
            if obj.type == 'Pickup':
                pos = pygame.math.Vector2(obj.x, obj.y)
                surf = image_to_sprite_dict(png('data/assets/png/misc/not_found.png'))
                p = Pickup(surf, obj_layers_to_groups[obj_layer_name], pos, active=obj.active, ability=obj.ability)
                tmx_pickups.append(p)

    return tmx_tiles, tmx_decor, tmx_triggers, tmx_spawners, tmx_limits, tmx_walls, tmx_enemy_walls, tmx_spikes, tmx_pickups, tmx_text