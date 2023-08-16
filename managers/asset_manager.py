import random

import pygame

ASSET_PATHS = {
    'hut': 'assets/buildings/hut2.png',
    'road': 'assets/buildings/road.png',
    'church': 'assets/buildings/church.png',
    # You can add more assets here as needed
}


class AssetManager:
    def __init__(self):
        self.assets = {}

    def get_asset(self, name):
        asset = self.assets.get(name)
        if asset is None:
            # If the asset is not loaded yet, load it now
            self._load_asset(name)
            asset = self.assets.get(name)
        return asset

    def _load_asset(self, name):
        path = ASSET_PATHS.get(name)
        if path:
            self.assets[name] = pygame.image.load(path).convert_alpha()
        else:
            raise ValueError(f"No asset found for name: {name}")


def load_road_subset(asset_manager: AssetManager):
    num = random.choice([4, 5])
    road_map = asset_manager.get_asset('road')

    sprite_width = 24
    sprite_height = 24

    sprite = road_map.subsurface(pygame.Rect(num * sprite_width, 0, sprite_width, sprite_height))
    return sprite
