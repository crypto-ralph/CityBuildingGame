import sys

import pygame
from game_settings import GameSettings, GameState
from interface.main_menu_ui import MainMenu
from interface.ingame_settings_menu_ui import ResolutionMenu


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
                        GameSettings.GAME_STATE = GameState.GAME
                        running = False
                    elif menu.settings_button.is_clicked(event.pos):
                        # Open the settings window
                        GameSettings.GAME_STATE = GameState.SETTINGS
                        running = False
                    elif menu.exit_button.is_clicked(event.pos):
                        GameSettings.GAME_STATE = GameState.EXIT_GAME
                        running = False
                    elif menu.credits_button.is_clicked(event.pos):
                        # Give credit where credit is due
                        print(
                            "Credits: This game was created with the help of ChatGPT, a large language model trained by OpenAI."
                        )

        for button in menu.menu_buttons:
            button.handle_hovered(pygame.mouse.get_pos())
        menu.draw()


def settings_menu(screen):
    menu = ResolutionMenu(screen)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen with black

        menu.highlight_current_resolution()
        for button in menu.buttons:
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
                                GameSettings.GAME_STATE = GameState.MAIN_MENU
                                running = False
                                continue
                            # Set the resolution and update the screen
                            current_resolution = tuple(map(int, button.text.split("x")))
                            GameSettings.set_screen_dimensions(current_resolution[0], current_resolution[1])
                            pygame.display.set_mode(current_resolution)

                            # Update button positions based on the new resolution
                            menu.update_menu_rect()
                            menu.update_menu_positions()
        menu.draw()
