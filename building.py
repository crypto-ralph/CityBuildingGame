import pygame

from map import TILE_SIZE, MAP_HEIGHT, MAP_WIDTH
from effects import generate_shadow


class BuildingPreview:
    def __init__(self, asset):
        self.image = asset
        # Here you are calling the tint_image function with a color parameter to get tinted images
        self.tinted_image_green = self.tint_image((0, 255, 0, 128))
        self.tinted_image_red = self.tint_image((255, 0, 0, 128))

    def tint_image(self, color):
        """Tints the building image with the given color."""
        tinted_image = self.image.copy()
        tinted_image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted_image


class Building:
    def __init__(self, name, width, height, cost, image):
        self.name = name
        self.width = width
        self.height = height
        self.x = None
        self.y = None
        self.cost = cost
        self.image = image
        self.tinted_image = None
        self.income = 0

    def get_income(self):
        return self.income

    def get_citizens(self):
        return 0

    def draw(self, surface, camera_offset_x, camera_offset_y):
        # Generate shadow for the building
        shadow, shadow_offset = generate_shadow(self.image)

        # Draw the shadow considering the camera offset
        surface.blit(shadow, ((self.x * TILE_SIZE + shadow_offset[0]) - camera_offset_x, (self.y * TILE_SIZE + shadow_offset[1]) - camera_offset_y))

        # Draw the building considering the camera offset
        surface.blit(self.image, ((self.x * TILE_SIZE) - camera_offset_x, (self.y * TILE_SIZE) - camera_offset_y))


class House(Building):
    def __init__(self, asset, x=None, y=None):
        super().__init__(name="House", width=3, height=3, cost=100, image=asset)
        self.x = x
        self.y = y
        self.income = -10
        self.citizens = 4

    def get_citizens(self):
        return self.citizens
