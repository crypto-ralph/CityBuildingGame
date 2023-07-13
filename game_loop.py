import sys

import pygame

from building import House
from game_manager import GameManager, BuildingManager
from game_settings import GameSettings
from map import TILE_SIZE
from ui import UI

FPS = 60

version_text = f"Version: 1.0"
build_text = f"Build: 2022-03-06"

game_manager = GameManager()
building_manager = BuildingManager()

UI_BUTTON_COLOR = (150, 150, 150)
UI_BACKGROUND_COLOR = (200, 200, 200)


def game_loop(game_map, game_clock, screen):
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
    hut_placing = False
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

        dt = game_clock.tick(FPS) / 1000.0
        current_time = pygame.time.get_ticks()
        if current_time >= income_update_time:
            # Update income if the interval has passed
            game_manager.money += building_manager.get_income()
            ui.money = game_manager.money
            ui.income = building_manager.get_income()
            ui.citizens = game_manager.citizens
            income_update_time = current_time + game_manager.income_update_interval

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hut_placing:
                        building_manager.add_building(House(tile_x, tile_y))
                        hut_placing = False

                    if ui.ui_exit_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "menu"
                        running = False
                    if ui.hut_button.is_clicked(event.pos):
                        hut_placing = True
                        # x, y = 5, 5
                        # coords = [(y + row, x + col) for row in range(building.height) for col in range(building.width)]
                        # if building.can_place(coords, map_data):
                        #     building.place(coords, map_data)
                        #     building_manager.add_building(building)
                    else:
                        if prev_highlighted_tile:
                            prev_highlighted_tile.set_clicked(True)
                            clicked_tile = prev_highlighted_tile
                            print("clicked")
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


        tile = game_map.map.get_tile_at(tile_x, tile_y)

        if tile and tile != prev_highlighted_tile:
            if prev_highlighted_tile:
                prev_highlighted_tile.set_highlighted(False)
            tile.set_highlighted(True)
            prev_highlighted_tile = tile

        # Update the game state
        # game_map.update(dt)
        draw_game(screen, game_map, ui, camera_offset_x, camera_offset_y)

        if hut_placing:
            hut = House()
            screen.blit(hut.image, (tile_x * TILE_SIZE, tile_y * TILE_SIZE))

        game_map.map.buildings = building_manager.buildings


        # Update the display
        pygame.display.flip()

        # Tick the game clock
        game_clock.tick(FPS)


def draw_game(screen, game_map, ui, camera_offset_x, camera_offset_y):
    screen.fill((0, 0, 0))  # Clear the screen with black

    game_map.draw(screen, camera_offset_x, camera_offset_y)

    # Draw the version and build number in the bottom right corner
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(f"Version: {version_text} Build: {build_text}", True, (0, 0, 0))
    screen.blit(
        text,
        (
            game_map.map.width - text.get_width() - 5,
            game_map.map.height - text.get_height() - 5,
        ),
    )

    # Draw the UI buttons
    pygame.draw.rect(
        screen,
        UI_BACKGROUND_COLOR,
        (GameSettings.GAME_WORLD_WIDTH, 0, ui.UI_AREA_WIDTH, ui.UI_AREA_HEIGHT),
    )

    # Draw UI
    ui.draw(screen)
    ui.draw_top_bar(screen)

    # Update the display
    pygame.display.update()
