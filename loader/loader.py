import pygame

def png(path):
    return pygame.image.load(path).convert_alpha()

def load_sprites(sprite_list):
    sprites = []
    for path in sprite_list:
        image = png(path)
        sprites.append(image)
    return sprites

def glsl_to_string(path):
    with open(path, "r") as glsl:
         string = glsl.read()
    return string