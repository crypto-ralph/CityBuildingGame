import math
import random
import pygame
import noise

MAP_WIDTH = 35
MAP_HEIGHT = 35
TILE_SIZE = 24
OCTAVES = 6
FREQUENCY = 16.0
WATER_THRESHOLD = 0.05

TILE_IMAGES = {
    "grass": pygame.image.load("assets/grass.png"),
    "water": pygame.image.load("assets/water.png"),
    # "forest": pygame.image.load("forest.png"),
    # Add more tile types and images as needed
}


class Tile:
    def __init__(self, tile_type="grass"):
        self.elevation = 0
        self.type = tile_type
        self.color = self.get_color()
        self.highlighted = False
        self.clicked = False

    def get_color(self):
        if self.type == "grass":
            green = int(255 * (self.elevation + 0.5) / 1.5)
            return 0, green, 0
        elif self.type == "water":
            blue = int(255 * (1 - self.elevation))
            return 0, 0, max(0, blue)
        else:
            # default color is black
            return 0, 0, 0

    def set_elevation(self, elevation):
        self.elevation = elevation
        self.color = self.get_color()

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, self.color, (x, y, TILE_SIZE, TILE_SIZE))
        border_color = (255, 255, 255) if not self.clicked else (200, 200, 200)
        if self.highlighted:
            pygame.draw.rect(surface, border_color, (x, y, TILE_SIZE, TILE_SIZE), 2)  # Draw a border

    def set_highlighted(self, highlighted):
        self.highlighted = highlighted

    def set_clicked(self, clicked):
        self.clicked = clicked


class Map:
    def __init__(self, width, height):
        self.elevation = None
        self.width = width
        self.height = height
        self.tiles = [[Tile() for y in range(height)] for x in range(width)]
        self.buildings = []
        self.generate_map()

    def generate_map(self):
        # Generate the tiles and set their elevation using Perlin noise
        for x in range(self.width):
            for y in range(self.height):
                elevation = noise.pnoise2(
                    x / FREQUENCY, y / FREQUENCY, OCTAVES
                )
                tile = Tile()
                if elevation < WATER_THRESHOLD:
                    tile.type = "water"
                tile.set_elevation((elevation + 1) / 2)  # Normalize elevation to [0, 1]
                self.tiles[x][y] = tile

    def draw(self, surface, camera_offset_x, camera_offset_y):
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[x][y].draw(
                    surface,
                    x * TILE_SIZE - camera_offset_x,
                    y * TILE_SIZE - camera_offset_y
                )

        for building in self.buildings:
            building.draw(surface)

    def add_building(self, building):
        self.buildings.append(building)

    def get_tile_at(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        else:
            return self.tiles[x][y]

    def get_building_at(self, x, y):
        for building in self.buildings:
            if building.x == x and building.y == y:
                return building
        return None


class GameMap:
    def __init__(self, width, height):
        self.map = Map(width, height)

    # def update(self, dt):
    #     for building in self.map.buildings:
    #         building.update(dt)

    def draw(self, surface, camera_offset_x, camera_offset_y):
        self.map.draw(surface, camera_offset_x, camera_offset_y)
