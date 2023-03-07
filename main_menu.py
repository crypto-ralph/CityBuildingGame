import sys

import pygame
from button import Button
from game_settings import GameSettings

UI_BUTTON_COLOR = (150, 150, 150)
BUTTON_PADDING = 20
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Create the version and build number text
pygame.font.init()
version_text = f"Version: 1.0"
build_text = f"Build: 2022-03-06"
version_font = pygame.font.Font(None, 20)
version_surface = version_font.render(version_text, True, (255, 255, 255))
version_rect = version_surface.get_rect(bottomright=(GameSettings.SCREEN_WIDTH - BUTTON_PADDING, GameSettings.SCREEN_HEIGHT - BUTTON_PADDING))
build_font = pygame.font.Font(None, 20)
build_surface = build_font.render(build_text, True, (255, 255, 255))
build_rect = build_surface.get_rect(bottomright=(GameSettings.SCREEN_WIDTH - BUTTON_PADDING, GameSettings.SCREEN_HEIGHT - BUTTON_PADDING // 2))


def main_menu(screen):
    # Create the buttons if they were not passed in as arguments
    start_button = Button(x=50, y=50, width=200, height=50, text="Start Game", button_color=UI_BUTTON_COLOR)
    settings_button = Button(x=50, y=120, width=200, height=50, text="Settings", button_color=UI_BUTTON_COLOR)
    exit_button = Button(x=50, y=190, width=200, height=50, text="Exit Game", button_color=UI_BUTTON_COLOR)
    credits_button = Button(x=50, y=260, width=200, height=50, text="Credits", button_color=UI_BUTTON_COLOR)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "game"
                        running = False
                    elif settings_button.is_clicked(event.pos):
                        print("Settings button clicked")
                    elif exit_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "exit_game"
                        running = False
                    elif credits_button.is_clicked(event.pos):
                        print("Credits button clicked")

        # Draw the screen
        screen.fill((0, 0, 0))
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)
        credits_button.draw(screen)
        screen.blit(version_surface, version_rect)
        screen.blit(build_surface, build_rect)
        pygame.display.flip()
