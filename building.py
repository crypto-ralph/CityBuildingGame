import pygame

from map import TILE_SIZE, MAP_HEIGHT, MAP_WIDTH


class Building:
    def __init__(self, name, width, height, cost):
        self.name = name
        self.width = width
        self.height = height
        self.cost = cost
        self.image = pygame.Surface((width * TILE_SIZE, height * TILE_SIZE))
        self.image.fill((255, 0, 0))  # Replace with actual building image
        self.income = 0

    def can_place(self, x, y, map_data):
        # Check if the building can be placed at the given coordinates
        for row in range(y, y + self.height):
            for column in range(x, x + self.width):
                if (
                    row >= MAP_HEIGHT
                    or column >= MAP_WIDTH
                    or map_data[row][column] != 1
                ):
                    return False
        return True

    def place(self, x, y, map_data):
        # Place the building on the map at the given coordinates
        if self.can_place(x, y, map_data):
            for row in range(y, y + self.height):
                for column in range(x, x + self.width):
                    map_data[row][
                        column
                    ] = 2  # Use a new value to indicate the building
            return True
        else:
            return False

    def get_income(self):
        return self.income
