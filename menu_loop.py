import sys

import pygame
from game_settings import GameSettings
from ui.main_menu_ui import MainMenu
from ui.settings_menu_ui import SettingsMenu

UI_BUTTON_COLOR = (150, 150, 150)
HOVER_BUTTON_COLOR = (200, 200, 200)
BUTTON_PADDING = 20
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Create the version and build number text
pygame.font.init()
version_text = f"Version: 1.5"
build_text = f"Build: 2022-07-14"
version_font = pygame.font.Font(None, 20)
version_surface = version_font.render(version_text, True, (255, 255, 255))
version_rect = version_surface.get_rect(
    bottomright=(
        GameSettings.SCREEN_WIDTH - BUTTON_PADDING,
        GameSettings.SCREEN_HEIGHT - BUTTON_PADDING,
    )
)
build_font = pygame.font.Font(None, 20)
build_surface = build_font.render(build_text, True, (255, 255, 255))
build_rect = build_surface.get_rect(
    bottomright=(
        GameSettings.SCREEN_WIDTH - BUTTON_PADDING,
        GameSettings.SCREEN_HEIGHT - BUTTON_PADDING // 2,
    )
)


def main_menu(screen):
    menu = MainMenu(screen)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen with black
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu.start_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "game"
                        running = False
                    elif menu.settings_button.is_clicked(event.pos):
                        # Open the settings window
                        settings_menu_loop(screen)
                    elif menu.exit_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "exit_game"
                        running = False
                    elif menu.credits_button.is_clicked(event.pos):
                        # Give credit where credit is due
                        print(
                            "Credits: This game was created with the help of ChatGPT, a large language model trained by OpenAI."
                        )

        for button in menu.menu_buttons:
            button.handle_hovered(pygame.mouse.get_pos())

        menu.draw()


def settings_menu_loop(screen):
    menu = SettingsMenu(screen)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen with black
        current_resolution = (GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)


        # Highlight current resolution
        for button in menu.buttons:
            if button.text == f"{current_resolution[0]}x{current_resolution[1]}":
                button.set_color((100, 100, 100))
            else:
                button.set_color(UI_BUTTON_COLOR)
                button.handle_hovered(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in menu.buttons:
                        if button.is_clicked(event.pos):
                            if button.text == "Back":
                                running = False
                                continue
                            # Set the resolution and update the screen
                            current_resolution = tuple(map(int, button.text.split("x")))
                            GameSettings.set_screen_dimensions(
                                current_resolution[0], current_resolution[1]
                            )
                            pygame.display.set_mode(current_resolution)

                            # Update button positions based on the new resolution
                            menu.update_menu_positions()
        menu.draw()
