import pygame

from map import TILE_SIZE, MAP_HEIGHT, MAP_WIDTH


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
        self.income = 0

    def can_place(self, coords, map_data):
        # Check if the building can be placed at the given coordinates
        for coord in coords:
            row, column = coord
            if (
                row >= MAP_HEIGHT
                or column >= MAP_WIDTH
                or map_data[row][column] != 1
            ):
                return False
        return True

    def place(self, coords, map_data):
        # Place the building on the map at the given coordinates
        if self.can_place(coords, map_data):
            for coord in coords:
                row, column = coord
                map_data[row][
                    column
                ] = 2  # Use a new value to indicate the building
            return True
        else:
            return False

    def get_income(self):
        return self.income

    def draw(self, surface):
        surface.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))



class House(Building):
    def __init__(self, x=None, y=None):
        super().__init__(name="House", width=3, height=3, cost=100, image_path="assets/buildings/hut.png")
        self.x = x
        self.y = y
        self.income = 10  # Houses generate income for the player
