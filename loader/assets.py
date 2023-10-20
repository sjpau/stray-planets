from utils.utils import collect_image_paths
from loader.loader import png, load_sprites
from utils.sprites import SpriteStack

sprites_background_layers = load_sprites(sorted(collect_image_paths('data/assets/png/background/sodium/parallax/')))
sprites_clouds = sorted(collect_image_paths('data/sprites/env/clouds/sodium/'))

sprites_env_dust = {
    'dust': SpriteStack(sorted(collect_image_paths('data/assets/sprites/env/dust/sodium/'))),
}

sprites_player = {
    'idle': SpriteStack(sorted(collect_image_paths('data/assets/sprites/player/idle/'))),
}