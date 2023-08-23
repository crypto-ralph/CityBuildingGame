import sys

import pygame

from geometry import Size
from loops.ingame_menu_loop import ingame_settings_menu_loop
from managers.asset_manager import AssetManager
from managers.game_manager import GameManager, BuildingManager
from game_settings import GameSettings, GameState
from interface.in_game_ui import UI
from managers.road_manager import RoadManager
from map import TILE_SIZE

FPS = 60


def game_loop(game_map, game_clock, screen):
    # Create managers here to avoid keeping values
    game_manager = GameManager()
    asset_manager = AssetManager()
    road_manager = RoadManager(asset_manager)
    building_manager = BuildingManager(asset_manager, game_manager)

    screen_size = Size(GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)
    ui = UI(screen_size, asset_manager)

    ui.money = game_manager.money
    income_update_time = pygame.time.get_ticks() + game_manager.income_update_interval

    prev_highlighted_tile = None
    clicked_tile = None

    camera_offset_x = 0
    camera_offset_y = 0

    prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()

    right_mouse_button_down = False
    running = True

    while running:
        if GameSettings.GAME_STATE == GameState.INGAME_SETTINGS:
            ingame_settings_menu_loop(screen)
        # Map boundaries
        max_camera_offset_x = game_map.width * TILE_SIZE - GameSettings.GAME_WORLD_WIDTH
        max_camera_offset_y = game_map.height * TILE_SIZE - GameSettings.GAME_WORLD_HEIGHT
        min_camera_offset_x = 0
        min_camera_offset_y = 0 - ui.top_bar_height

        mouse_pos = pygame.mouse.get_pos()

        mouse_x, mouse_y = mouse_pos
        tile_x, tile_y = (
            (mouse_x + camera_offset_x) // TILE_SIZE,
            (mouse_y + camera_offset_y) // TILE_SIZE,
        )

        tile = game_map.get_tile_at(tile_x, tile_y)

        if building_manager.current_building is not None:
            building_manager.check_placement(tile_x, tile_y, mouse_x, mouse_y, game_map)

        current_time = pygame.time.get_ticks()
        if current_time >= income_update_time:
            # Update income if the interval has passed
            game_manager.money += game_manager.income
            income_update_time = current_time + game_manager.income_update_interval

        ui.money = game_manager.money
        ui.income = game_manager.income
        ui.citizens = game_manager.citizens

        for button in ui.building_buttons:
            button.handle_hovered(mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if building_manager.current_building is not None:
                        tiles_to_check = building_manager.get_tiles_for_building(tile_x, tile_y, game_map)
                        building_manager.place_building(tile_x, tile_y, tiles_to_check)
                    if road_manager.road_building_mode:
                        if road_manager.start_point is None:
                            road_manager.start_building((tile_x, tile_y))
                        else:
                            road_manager.build_road()
                    if ui.settings_button.is_clicked(event.pos):
                        GameSettings.GAME_STATE = GameState.INGAME_SETTINGS
                    if ui.hut_button.is_clicked(event.pos):
                        building_manager.select_building("hut")
                    if ui.church_button.is_clicked(event.pos):
                        building_manager.select_building("church")
                    if ui.road_button.is_clicked(event.pos):
                        road_manager.toggle_road_building_mode()
                    else:
                        if prev_highlighted_tile:
                            prev_highlighted_tile.set_clicked(True)
                            clicked_tile = prev_highlighted_tile
                elif event.button == 3:
                    right_mouse_button_down = True
                    prev_mouse_x, prev_mouse_y = mouse_pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if clicked_tile:
                        clicked_tile.set_clicked(False)
                        clicked_tile = None
                elif event.button == 3:
                    right_mouse_button_down = False
            elif event.type == pygame.MOUSEMOTION:
                if road_manager.road_building_mode and road_manager.start_point is not None:
                    road_manager.set_preview_path(game_map, (tile_x, tile_y))

        # Handle camera movement
        if right_mouse_button_down:
            if (
                game_map.width * TILE_SIZE > GameSettings.GAME_WORLD_WIDTH
                and game_map.height * TILE_SIZE > GameSettings.GAME_WORLD_HEIGHT
            ):
                mouse_x, mouse_y = mouse_pos
                dx, dy = prev_mouse_x - mouse_x, prev_mouse_y - mouse_y
                camera_offset_x += dx
                camera_offset_y += dy

                if camera_offset_x < min_camera_offset_x:
                    camera_offset_x = min_camera_offset_x
                if camera_offset_x > max_camera_offset_x:
                    camera_offset_x = max_camera_offset_x

                if camera_offset_y < min_camera_offset_y:
                    camera_offset_y = min_camera_offset_y
                if camera_offset_y > max_camera_offset_y:
                    camera_offset_y = max_camera_offset_y

                prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

        if building_manager.current_building is None:
            if tile and tile != prev_highlighted_tile:
                if prev_highlighted_tile:
                    prev_highlighted_tile.set_highlighted(False)
                tile.set_highlighted(True)
                prev_highlighted_tile = tile
        else:
            tile.set_highlighted(False)

        if GameSettings.GAME_STATE == GameState.EXIT_PLAY:
            GameSettings.GAME_STATE = GameState.MAIN_MENU
            running = False
        else:
            # Draw Map and UI
            draw_game(
                screen,
                game_map,
                ui,
                building_manager,
                game_manager,
                road_manager,
                camera_offset_x,
                camera_offset_y,
                tile_x,
                tile_y,
                mouse_pos,
            )

            # Update the display
            pygame.display.flip()

            # Tick the game clock
            game_clock.tick(FPS)


def draw_game(
    screen,
    game_map,
    ui,
    building_manager,
    game_manager,
    road_manager,
    camera_offset_x,
    camera_offset_y,
    tile_x,
    tile_y,
    mouse_pos,
):
    screen.fill((255, 255, 255))

    # Hide the mouse cursor when it is over the map and show it when over the UI
    mouse_x, mouse_y = mouse_pos
    if 0 <= mouse_x < GameSettings.GAME_WORLD_WIDTH:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    game_map.draw(screen, camera_offset_x, camera_offset_y)

    for road in road_manager.roads:
        road.draw(screen, camera_offset_x, camera_offset_y)

    for building in building_manager.buildings:
        building.draw(screen, camera_offset_x, camera_offset_y)

    if building_manager.current_building is not None and mouse_x < GameSettings.GAME_WORLD_WIDTH:
        screen.blit(
            building_manager.get_current_preview(),
            (
                tile_x * TILE_SIZE - camera_offset_x,
                tile_y * TILE_SIZE - camera_offset_y,
            ),
        )

    road_manager.draw_preview(screen, camera_offset_x, camera_offset_y)

    ui.draw(screen, game_manager.money, game_manager.income, game_manager.citizens)

    for button in ui.building_buttons:
        if button.hovered and hasattr(button, "info_box"):
            button.info_box.draw(screen, line_spacing=7)
