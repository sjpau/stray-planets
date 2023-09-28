import pygame    
import moderngl
    
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