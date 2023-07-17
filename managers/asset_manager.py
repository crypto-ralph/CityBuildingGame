import pygame

ASSET_PATHS = {
    'hut': 'assets/buildings/hut.png',
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