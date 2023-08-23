import sys
from functools import partial

import pygame

from game_settings import GameSettings, GameState
from interface.ingame_settings_menu_ui import SettingsMenu, ResolutionMenu


def get_button_by_text(buttons_group, target_text):
    for button in buttons_group:
        if button.text == target_text:
            return button
    return None


def change_resolution(screen):
    ingame_resolution_menu_loop(screen)


def exit_game():
    GameSettings.GAME_STATE = GameState.EXIT_PLAY
    return False


def exit_settings():
    GameSettings.GAME_STATE = GameState.GAME
    return False


def ingame_settings_menu_loop(screen):
    menu = SettingsMenu(screen)

    # Button to action mapping by text
    button_actions = {
        "Resolution": partial(change_resolution, screen),
        "Back To Game": partial(exit_settings),
        "Exit Game": partial(exit_game)
        # ... add other buttons and their actions here using their text
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for text, action in button_actions.items():
                    button = get_button_by_text(menu.buttons, text)
                    if button and button.is_clicked(event.pos):
                        result = action()
                        if result is False:  # if the action returns False, we exit the loop
                            running = False
                        break  # exit the loop once a button action is executed
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the settings menu on top
        menu.draw()


def ingame_resolution_menu_loop(screen):
    resolution_menu = ResolutionMenu(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if resolution_menu.back_button.is_clicked(event.pos):
                        resolution_menu = ResolutionMenu(screen)
                        running = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        resolution_menu.draw()
