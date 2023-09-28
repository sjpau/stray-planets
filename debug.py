import pygame
pygame.init()

status = True
font = pygame.font.Font(None, 30)

def display(surf, info, y = 10, bg = 'Black', fg = 'White', x = 10):
    display_surf = surf
    debug_surf = font.render(str(info), True, fg)
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surf, bg, debug_rect)
    display_surf.blit(debug_surf, debug_rect)
