from typing import Tuple, List

import pygame

from building import Road
from managers.game_manager import can_place
from map import TILE_SIZE


def bresenham_line_path(start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Compute a line using Bresenham's line algorithm between two points.

    :param start: A tuple representing the x and y coordinates of the start point.
    :type start: Tuple[int, int]
    :param end: A tuple representing the x and y coordinates of the end point.
    :type end: Tuple[int, int]
    :return: List of tuples representing the coordinates of the line points.
    :rtype: List[Tuple[int, int]]
    """
    x1, y1 = start
    x2, y2 = end
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points


def manhattan_path(start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Compute a path that follows grid lines (only horizontal and vertical movements) between two points.
    This pathfinding approach is based on the Manhattan Distance method.

    :param start: A tuple representing the x and y coordinates of the start point.
    :type start: Tuple[int, int]
    :param end: A tuple representing the x and y coordinates of the end point.
    :type end: Tuple[int, int]
    :return: List of tuples representing the coordinates of the line points.
    :rtype: List[Tuple[int, int]]
    """
    x1, y1 = start
    x2, y2 = end
    path = []

    # Move horizontally
    while x1 != x2:
        path.append((x1, y1))
        x1 += 1 if x1 < x2 else -1

    # Move vertically
    while y1 != y2:
        path.append((x1, y1))
        y1 += 1 if y1 < y2 else -1

    path.append((x1, y1))

    return path

class RoadManager:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        self.road_building_mode = False
        self.start_point = None
        self.can_place_road = True
        self.roads = []
        self.preview_path = None # Add this property
        self.path_tiles = None

    def toggle_road_building_mode(self):
        self.road_building_mode = not self.road_building_mode
        self.start_point = None
        self.preview_path = None  # Clear the preview path when toggling the mode

    def start_building(self, start_point):
        self.start_point = start_point

    def calculate_path(self, end_point):
        return manhattan_path(self.start_point, end_point)

    def build_road(self):

        if self.can_place_road:
            for coords, tile in self.path_tiles.items():
                x, y = coords
                road = Road(x, y)
                self.roads.append(road)
                # Mark the tile as occupied
                tile.occupied = road.type
        self.start_point = None
        self.road_building_mode = False
        self.preview_path = None  # Clear the preview path when building is done
        self.path_tiles = None
    def set_preview_path(self, game_map, end_point):
        """Calculate the path for preview and store it."""
        self.preview_path = self.calculate_path(end_point)
        self.path_tiles = {(point[0], point[1]): game_map.get_tile_at(point[0], point[1]) for point in self.preview_path}
        self.can_place_road = can_place(self.path_tiles.values(), Road)

    def draw_preview(self, surface, camera_offset_x, camera_offset_y):
        """Draw the road preview using the calculated path."""

        if self.preview_path:
            color = (255, 100, 100) if not self.can_place_road else (200, 200, 200)
            for x, y in self.preview_path:
                pygame.draw.rect(surface, color, ((x * TILE_SIZE) - camera_offset_x, (y * TILE_SIZE) - camera_offset_y, TILE_SIZE, TILE_SIZE))