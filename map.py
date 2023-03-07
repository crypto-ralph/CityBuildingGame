# Define the map size
import math
import random

import pygame

MAP_WIDTH = 20
MAP_HEIGHT = 20
TILE_SIZE = 32

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

    def draw(self, surface, x, y):
        tile_image = TILE_IMAGES[self.type]
        surface.blit(tile_image, (x, y))


class Map:
    def __init__(self, width, height, water_proportion):
        self.elevation = None
        self.width = width
        self.height = height
        self.tiles = [[Tile() for y in range(height)] for x in range(width)]
        self.buildings = []
        self.generate_map(water_proportion)

    def generate_map(self, water_proportion):
        # Generate the tiles and set their elevation randomly
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile()
                if random.random() < water_proportion:
                    tile.type = "water"
                tile.elevation = random.random()
                self.tiles[x][y] = tile

        # Generate the river
        start_x = self.width // 2
        start_y = 0
        end_x = start_x
        end_y = self.height - 1

        # Set the elevation of the tiles along the river to be lower
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[x][y]
                distance_to_river = abs(
                    (end_y - start_y) * x - (end_x - start_x) * y + end_x * start_y - end_y * start_x) / math.sqrt(
                    (end_y - start_y) ** 2 + (end_x - start_x) ** 2)
                if distance_to_river < 20:
                    tile.elevation -= 0.1 * (20 - distance_to_river) / 20

                    # Make sure the elevation stays within the valid range of 0 to 1
                    tile.elevation = max(0, min(1, tile.elevation))

    def draw(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[x][y].draw(surface, x * TILE_SIZE, y * TILE_SIZE)

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
        self.map = Map(width, height, 0.3)

    def update(self, dt):
        for building in self.map.buildings:
            building.update(dt)

    def draw(self, surface):
        self.map.draw(surface)
