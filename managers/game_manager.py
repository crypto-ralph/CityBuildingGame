import pygame

from building import Building, BuildingPreview, House
from managers.asset_manager import AssetManager
from map import Map, Tile, TILE_SIZE


class BuildingManager:
    def __init__(self, asset_manager: AssetManager):
        self.asset_manager = asset_manager
        self.current_building = None
        self.building_preview = None
        self.building_can_be_placed = False
        self.buildings = []

    def select_building(self, building_type: str):
        asset = self.asset_manager.get_asset(building_type)
        self.current_building = House(asset)
        self.building_preview = BuildingPreview(asset)

    def clear_current_building(self):
        self.current_building = None
        self.building_preview = None
        self.building_can_be_placed = False

    def place_building(self, x, y, tiles):
        if self.building_can_be_placed:
            self.current_building.x = x
            self.current_building.y = y

            for tile in tiles:
                tile.occupied = True

            self.buildings.append(self.current_building)
            self.clear_current_building()

    def remove_building(self, building):
        self.buildings.remove(building)

    def check_placement(self, tile_x, tile_y, game_map):
        if self.current_building:
            tiles_to_check = self.get_tiles_for_building(tile_x, tile_y, game_map)
            self.building_can_be_placed = self.can_place(tiles_to_check)

    def get_current_preview(self):
        if self.building_can_be_placed:
            return self.building_preview.tinted_image_green
        else:
            return self.building_preview.tinted_image_red

    def can_place(self, tiles_to_check):
        # Iterate over all tiles in the list
        for tile in tiles_to_check:
            # Check if the tile type is suitable and if it's not occupied
            if tile.type != "grass" or tile.occupied:
                return False
        # If all tiles are suitable, return True
        return True

    def get_tiles_for_building(self, tile_x: int, tile_y: int, game_map: Map):
        tiles_to_check = []

        # Iterate over all tiles within the building's dimensions
        for dx in range(self.current_building.width):
            check_tile_x = tile_x + dx
            for dy in range(self.current_building.height):
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

    def get_citizens(self):
        total_citizens = 0
        for building in self.buildings:
            income = building.get_citizens()
            total_citizens += income
        return total_citizens


class GameManager:
    # Set up the income update interval
    income_update_interval = 10000  # 10 seconds

    def __init__(self, money: int = 10000):
        self.money = money
        self.citizens = 0

    def add_income(self, income):
        self.money += income
