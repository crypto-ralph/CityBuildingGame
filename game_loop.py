import sys

import pygame

from building import House
from game_manager import GameManager, BuildingManager
from game_settings import GameSettings
from interface.settings_menu import SettingsMenu
from map import TILE_SIZE
from ui import UI

FPS = 60

UI_BUTTON_COLOR = (150, 150, 150)
UI_BACKGROUND_COLOR = (200, 200, 200)


def game_loop(game_map, game_clock, screen):
    # Create managers here to avoid keeping values
    game_manager = GameManager()
    building_manager = BuildingManager()

    building_to_place = None
    building_can_be_placed = False

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
        max_camera_offset_x = game_map.map.width * TILE_SIZE - GameSettings.GAME_WORLD_WIDTH
        max_camera_offset_y = game_map.map.height * TILE_SIZE - GameSettings.GAME_WORLD_HEIGHT
        min_camera_offset_x = 0
        min_camera_offset_y = 0 - ui.TOP_BAR_HEIGHT

        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x, tile_y = (
            mouse_x // TILE_SIZE,
            mouse_y // TILE_SIZE,
        )

        tile = game_map.map.get_tile_at(tile_x, tile_y)

        dt = game_clock.tick(FPS) / 1000.0
        current_time = pygame.time.get_ticks()
        if current_time >= income_update_time:
            # Update income if the interval has passed
            game_manager.money += building_manager.get_income()
            ui.money = game_manager.money
            ui.income = building_manager.get_income()
            ui.citizens = game_manager.citizens
            income_update_time = current_time + game_manager.income_update_interval

        if building_to_place is not None:
            tiles_to_check = building_manager.get_tiles_for_building(tile_x, tile_y, building_to_place, game_map.map)
            building_can_be_placed = building_manager.can_place(tiles_to_check)
            if building_can_be_placed:
                building_to_place.tint_image((0, 255, 0, 128))
            else:
                building_to_place.tint_image((255, 0, 0, 128))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if building_to_place is not None and building_can_be_placed:
                        tiles_to_check = building_manager.get_tiles_for_building(tile_x, tile_y, building_to_place, game_map.map)
                        building_manager.place_building(building_to_place,tile_x, tile_y, tiles_to_check)
                        building_to_place.clear_tint()
                        building_to_place = None

                    if ui.settings_button.is_clicked(event.pos):
                        # Pause the game loop and enter the settings loop
                        ingame_settings_menu_loop(screen, game_map, ui, camera_offset_x, camera_offset_y)

                    if ui.ui_exit_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "menu"
                        running = False
                    if ui.hut_button.is_clicked(event.pos):
                        building_to_place = House()
                        building_to_place.tint_image((0, 255, 0, 128))
                    else:
                        if prev_highlighted_tile:
                            prev_highlighted_tile.set_clicked(True)
                            clicked_tile = prev_highlighted_tile
                elif event.button == 3:
                    right_mouse_button_down = True
                    prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if clicked_tile:
                        clicked_tile.set_clicked(False)
                        clicked_tile = None
                elif event.button == 3:
                    right_mouse_button_down = False


        # Hide the mouse cursor when it is over the map and show it when over the UI
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x < GameSettings.GAME_WORLD_WIDTH:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

        # Handle camera movement
        if right_mouse_button_down:
            if game_map.map.width * TILE_SIZE > GameSettings.GAME_WORLD_WIDTH and game_map.map.height * TILE_SIZE > GameSettings.GAME_WORLD_HEIGHT:
                mouse_x, mouse_y = pygame.mouse.get_pos()
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

        if tile and tile != prev_highlighted_tile:
            if prev_highlighted_tile:
                prev_highlighted_tile.set_highlighted(False)
            tile.set_highlighted(True)
            prev_highlighted_tile = tile

        # Update the game state
        # game_map.update(dt)
        # Draw Map and UI
        draw_game(screen, game_map, ui, building_manager.buildings, camera_offset_x, camera_offset_y)

        if building_to_place is not None:
            screen.blit(building_to_place.tinted_image, (tile_x * TILE_SIZE, tile_y * TILE_SIZE))

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

        # Draw the game
        draw_game(screen, game_map, ui, camera_offset_x, camera_offset_y)

        # Draw the settings menu on top
        menu.draw()

        # Flip the display
        pygame.display.flip()


def draw_game(screen, game_map, ui, buildings, camera_offset_x, camera_offset_y):
    screen.fill((0, 0, 0))
    game_map.draw(screen, camera_offset_x, camera_offset_y)
    ui.draw(screen)
    for building in buildings:
        building.draw(screen, camera_offset_x, camera_offset_y)
