import sys

import pygame

from managers.asset_manager import AssetManager
from managers.game_manager import GameManager, BuildingManager
from game_settings import GameSettings
from ui.settings_menu_ui import SettingsMenu
from ui.in_game_ui import UI
from map import TILE_SIZE

FPS = 60

UI_BUTTON_COLOR = (150, 150, 150)
UI_BACKGROUND_COLOR = (200, 200, 200)


def game_loop(game_map, game_clock, screen):
    # Create managers here to avoid keeping values
    game_manager = GameManager()
    asset_manager = AssetManager()
    building_manager = BuildingManager(asset_manager)

    # Create the UI buttons
    ui = UI(
        GameSettings.SCREEN_WIDTH,
        GameSettings.SCREEN_HEIGHT,
        ui_button_color=UI_BUTTON_COLOR,
        ui_background_color=UI_BACKGROUND_COLOR,
    )

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
        # Map boundaries
        max_camera_offset_x = game_map.width * TILE_SIZE - GameSettings.GAME_WORLD_WIDTH
        max_camera_offset_y = game_map.height * TILE_SIZE - GameSettings.GAME_WORLD_HEIGHT
        min_camera_offset_x = 0
        min_camera_offset_y = 0 - ui.TOP_BAR_HEIGHT

        mouse_pos = pygame.mouse.get_pos()

        mouse_x, mouse_y = mouse_pos
        tile_x, tile_y = (
            (mouse_x + camera_offset_x) // TILE_SIZE,
            (mouse_y + camera_offset_y) // TILE_SIZE,
        )

        tile = game_map.get_tile_at(tile_x, tile_y)

        dt = game_clock.tick(FPS) / 1000.0
        current_time = pygame.time.get_ticks()
        if current_time >= income_update_time:
            # Update income if the interval has passed
            game_manager.money += building_manager.get_total_income()
            ui.money = game_manager.money
            ui.income = building_manager.get_total_income()
            ui.citizens = building_manager.get_citizens()
            income_update_time = current_time + game_manager.income_update_interval

        if building_manager.current_building is not None:
            building_manager.check_placement(tile_x, tile_y, mouse_x, mouse_y, game_map)

        ui.hut_button.handle_hovered(mouse_pos)

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
                    if ui.settings_button.is_clicked(event.pos):
                        # Pause the game loop and enter the settings loop
                        ingame_settings_menu_loop(screen, game_map, ui, camera_offset_x, camera_offset_y)
                    if ui.ui_exit_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "menu"
                        running = False
                    if ui.hut_button.is_clicked(event.pos):
                        building_manager.select_building("hut")
                    if ui.road_button.is_clicked(event.pos):
                        building_manager.select_building("road")
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

        # Handle camera movement
        if right_mouse_button_down:
            if game_map.width * TILE_SIZE > GameSettings.GAME_WORLD_WIDTH and game_map.height * TILE_SIZE > GameSettings.GAME_WORLD_HEIGHT:
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

        # Draw Map and UI
        draw_game(screen, game_map, ui, building_manager, camera_offset_x, camera_offset_y, tile_x, tile_y, mouse_pos)

        # Update the display
        pygame.display.flip()

        # Tick the game clock
        game_clock.tick(FPS)


def ingame_settings_menu_loop(screen, game_map, ui, camera_offset_x, camera_offset_y):
    menu = SettingsMenu(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu.back_button.is_clicked(event.pos):
                        # Exit the settings loop
                        running = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the settings menu on top
        menu.draw()

        # Flip the display
        pygame.display.flip()


def draw_game(screen, game_map, ui, building_manager, camera_offset_x, camera_offset_y, tile_x, tile_y, mouse_pos):
    screen.fill((0, 0, 0))

    # Hide the mouse cursor when it is over the map and show it when over the UI
    mouse_x, mouse_y = mouse_pos
    if 0 <= mouse_x < GameSettings.GAME_WORLD_WIDTH:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    game_map.draw(screen, camera_offset_x, camera_offset_y)

    for building in building_manager.buildings:
        building.draw(screen, camera_offset_x, camera_offset_y)


    if building_manager.current_building is not None and mouse_x < GameSettings.GAME_WORLD_WIDTH:
        screen.blit(building_manager.get_current_preview(), (tile_x * TILE_SIZE - camera_offset_x, tile_y * TILE_SIZE - camera_offset_y))

    ui.draw(screen)


    if ui.hut_button.hovered:
        # draw info box here
        ui.draw_info_box(ui.hut_button.info_box, screen)
