from utils.utils import collect_image_paths
from loader.loader import png
from utils.sprites import SpriteStack

sprite_background = png('data/assets/png/background.png')
sprites_background_layers = sorted(collect_image_paths('data/png/parallax/'))
sprites_clouds = sorted(collect_image_paths('data/sprites/env/clouds/'))

sprites_env_dust = {
    'dust': SpriteStack(sorted(collect_image_paths('data/assets/sprites/env/dust/'))),
}

sprites_player = {
    'idle': SpriteStack(sorted(collect_image_paths('data/assets/sprites/player/idle/'))),
}