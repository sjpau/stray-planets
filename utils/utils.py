import pygame    
import moderngl
import os

def collect_image_paths(directory_path):
    image_paths = []
    for _, _, files in os.walk(directory_path):
        for filename in files:
            image_paths.append(os.path.join(directory_path, filename))

    return image_paths

    
def circle_surface(radius, color):
    if radius > 0:
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius, pygame.SRCALPHA)
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(100)
        return surf
    else:
        return None

def bool_dict_set_true(dic, key_to_true):
        for key in dic:
            if key_to_true == key:
                dic[key_to_true] = True
            else:
                dic[key] = False

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def surface_to_gl_texture(surf: pygame.Surface, ctx: moderngl.Context):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

def image_to_sprite_dict(surf: pygame.Surface) -> dict[pygame.Surface: [pygame.Mask, pygame.Mask]]:
    return { surf: [pygame.mask.from_surface(surf), pygame.mask.from_surface(pygame.transform.flip(surf, True, False))] }