"""
This module contains the code for generating a game map using Perlin noise.

Classes:

    Tile: Represents a single tile on the map. Each tile has a type (e.g., "grass", "water"),
          an elevation, and a color that depends on its type and elevation.

    Map: Represents the entire game map. The map is a 2D grid of Tile objects.

Constants:

    MAP_WIDTH, MAP_HEIGHT: The dimensions of the map, in tiles.

    TILE_SIZE: The size of a single tile, in pixels.

    OCTAVES: The number of octaves to use in the Perlin noise function. Increasing this
             value will increase the amount of detail in the terrain.

    FREQUENCY: The frequency of the Perlin noise function. Increasing this value will
               make the terrain features smaller and more frequent.

    WATER_THRESHOLD: The threshold elevation below which a tile is considered water.
                     Perlin noise returns values in the range -1 to 1. Adjust this
                     value to control the ratio of water to land on the map.
                     For example:
                        -1 results in nearly 100% land.
                         0 results in about 50% water and 50% land.
                         1 results in nearly 100% water.
                     Note: The distribution can vary a bit from map to map.
"""

import random
import pygame
import noise

MAP_WIDTH = 50
MAP_HEIGHT = 50
TILE_SIZE = 24
OCTAVES = 6
FREQUENCY = 16.0
WATER_THRESHOLD = -0.2
BEACH_THRESHOLD = -0.14  # Adjust this to control how wide the beaches are


class Tile:
    def __init__(self, tile_type="grass"):
        self.elevation = 0
        self.type = tile_type
        self.color = self.get_color()
        self.highlighted = False
        self.clicked = False
        self.occupied = None

    def get_color(self):
        if self.type == "grass":
            green = int(255 * (self.elevation + 0.5) / 1.5)
            return 0, green, 0
        elif self.type == "water":
            blue = int(255 * (1 - self.elevation))
            return 0, 0, max(0, blue)
        elif self.type == "sand":
            return 238, 214, 175
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
        self.noise_offset_x = random.uniform(0, 1000)  # Add these lines
        self.noise_offset_y = random.uniform(0, 1000)  # Add these lines
        self.generate_map()

    def generate_map(self):
        # Generate the tiles and set their elevation using Perlin noise
        for x in range(self.width):
            for y in range(self.height):
                elevation = noise.pnoise2(
                    (x + self.noise_offset_x) / FREQUENCY,
                    (y + self.noise_offset_y) / FREQUENCY,
                )
                tile = Tile()
                if elevation < WATER_THRESHOLD:
                    tile.type = "water"
                elif elevation < BEACH_THRESHOLD:
                    tile.type = "sand"
                tile.set_elevation((elevation + 1) / 2)  # Normalize elevation to [0, 1]
                self.tiles[x][y] = tile

    def get_tile_at(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        else:
            return self.tiles[x][y]

    def draw(self, surface, camera_offset_x, camera_offset_y):
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[x][y].draw(
                    surface,
                    x * TILE_SIZE - camera_offset_x,
                    y * TILE_SIZE - camera_offset_y
                )