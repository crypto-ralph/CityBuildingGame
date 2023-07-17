import pygame

from map import TILE_SIZE, MAP_HEIGHT, MAP_WIDTH
from effects import generate_shadow


class Building:
    def __init__(self, name, width, height, cost, image_path = None):
        self.name = name
        self.width = width
        self.height = height
        self.x = None
        self.y = None
        self.cost = cost
        # self.image = pygame.Surface((width * TILE_SIZE, height * TILE_SIZE))
        # self.image.fill((255, 0, 0))  # Replace with actual building image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.tinted_image = None
        self.income = 0

    def get_income(self):
        return self.income

    def draw(self, surface, camera_offset_x, camera_offset_y):
        # Generate shadow for the building
        shadow, shadow_offset = generate_shadow(self.image)

        # Draw the shadow considering the camera offset
        surface.blit(shadow, ((self.x * TILE_SIZE + shadow_offset[0]) - camera_offset_x, (self.y * TILE_SIZE + shadow_offset[1]) - camera_offset_y))

        # Draw the building considering the camera offset
        surface.blit(self.image, ((self.x * TILE_SIZE) - camera_offset_x, (self.y * TILE_SIZE) - camera_offset_y))

    def tint_image(self, color):
        """Tints the building image with the given color."""
        # Make a copy of the image
        self.tinted_image = self.image.copy()
        # Fill the copy with the tint color. The special_flags=pygame.BLEND_RGBA_MULT
        # will multiply the tint color with the surface color.
        self.tinted_image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

    def clear_tint(self):
        """Clears the tint from the building image."""
        self.tinted_image = None


class House(Building):
    def __init__(self, x=None, y=None):
        super().__init__(name="House", width=3, height=3, cost=100, image_path="assets/buildings/hut.png")
        self.x = x
        self.y = y
        self.income = 10  # Houses generate income for the player
