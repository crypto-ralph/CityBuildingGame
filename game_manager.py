import pygame

from building import Building
from map import Map, Tile, TILE_SIZE


class BuildingManager:
    def __init__(self):
        self.buildings = []

    def place_building(self, building: Building, x, y, tiles):
        building.x = x
        building.y = y

        for tile in tiles:
            tile.occupied = True

        self.buildings.append(building)

    def remove_building(self, building):
        self.buildings.remove(building)

    def can_place(self, tiles_to_check):
        # Iterate over all tiles in the list
        for tile in tiles_to_check:
            # Check if the tile type is suitable and if it's not occupied
            if tile.type != "grass" or tile.occupied:
                return False
        # If all tiles are suitable, return True
        return True

    def get_tiles_for_building(self, tile_x: int, tile_y: int, building: Building, game_map: Map):
        tiles_to_check = []

        # Iterate over all tiles within the building's dimensions
        for dx in range(building.width):
            check_tile_x = tile_x + dx
            for dy in range(building.height):
                check_tile_y = tile_y + dy
                # Check if the tile is within the map
                if check_tile_x < 0 or check_tile_y < 0 or check_tile_x >= game_map.width or check_tile_y >= game_map.height:
                    return None  # Return None if any tile is out of bounds

                # Get the tile at this position
                tile = game_map.tiles[check_tile_x][check_tile_y]

                # Add the tile to the list of tiles to check
                tiles_to_check.append(tile)

        return tiles_to_check


    def get_income(self):
        total_income = 0
        for building in self.buildings:
            income = building.get_income()
            total_income += income
        return total_income


class GameManager:
    # Set up the income update interval
    income_update_interval = 10000  # 10 seconds

    def __init__(self, money: int = 10000):
        self.money = money
        self.citizens = 0

    def add_income(self, income):
        self.money += income
