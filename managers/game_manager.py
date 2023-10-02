from building import BuildingPreview, House, Road, Building, Church
from managers.asset_manager import AssetManager, load_road_subset
from map import Map

buildings = {"hut": House}


class GameManager:
    # Set up the income update interval
    income_update_interval = 10000  # 10 seconds

    def __init__(self, money: int = 10000):
        self.money = money
        self.citizens = 0
        self.income = 0


def can_place(tiles_to_check, building):
    # Iterate over all tiles in the list
    for tile in tiles_to_check:
        # Check if the tile type is suitable and if it's not occupied
        if issubclass(building, Road):
            if tile.type != "grass" or tile.occupied not in (None, Road.type):
                return False
        else:
            if tile.type != "grass" or tile.occupied is not None:
                return False
    # If all tiles are suitable, return True
    return True


class BuildingManager:
    def __init__(self, asset_manager: AssetManager, game_manager: GameManager):
        self.asset_manager = asset_manager
        self.game_manager = game_manager
        self.current_building = None
        self.building_preview = None
        self.building_can_be_placed = False
        self.buildings = []
        self.roads = []

    def select_building(self, building_type: str):
        asset = self.asset_manager.get_asset(building_type)

        if building_type == "hut":
            self.current_building = House(asset)
        if building_type == "church":
            self.current_building = Church(asset)
        elif building_type == "road":
            asset = load_road_subset(self.asset_manager)
            self.current_building = Road(asset)

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
                tile.occupied = self.current_building.type

            if type(self.current_building) == Road:
                self.roads.append(self.current_building)
            else:
                self.buildings.append(self.current_building)

            if hasattr(self.current_building, "citizens"):
                self.game_manager.citizens += self.current_building.citizens
            if hasattr(self.current_building, "income"):
                self.game_manager.income += self.current_building.income
            self.game_manager.money -= self.current_building.cost
            self.clear_current_building()

    def remove_building(self, building):
        self.buildings.remove(building)

    def check_placement(self, tile_x, tile_y, mouse_x, mouse_y, game_map):
        if self.current_building:
            tiles_to_check = self.get_tiles_for_building(tile_x, tile_y, game_map)
            self.building_can_be_placed = can_place(tiles_to_check, type(self.current_building))

    def get_current_preview(self):
        if self.building_can_be_placed:
            return self.building_preview.tinted_image_green
        else:
            return self.building_preview.tinted_image_red

    def get_tiles_for_building(self, tile_x: int, tile_y: int, game_map: Map):
        tiles_to_check = []

        # Iterate over all tiles within the building's dimensions
        for dx in range(self.current_building.width):
            check_tile_x = tile_x + dx
            for dy in range(self.current_building.height):
                check_tile_y = tile_y + dy
                # Check if the tile is within the map
                if (
                    check_tile_x < 0
                    or check_tile_y < 0
                    or check_tile_x >= game_map.width
                    or check_tile_y >= game_map.height
                ):
                    return None  # Return None if any tile is out of bounds

                # Get the tile at this position
                tile = game_map.tiles[check_tile_x][check_tile_y]

                # Add the tile to the list of tiles to check
                tiles_to_check.append(tile)

        return tiles_to_check

    def get_citizens(self):
        total_citizens = 0
        for building in self.buildings:
            income = building.citizens
            total_citizens += income
        return total_citizens
