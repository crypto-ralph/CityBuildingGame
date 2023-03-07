import sys

import pygame

from button import Button
from game_settings import GameSettings

FPS = 60

version_text = f"Version: 1.0"
build_text = f"Build: 2022-03-06"

# Define the colors for the UI buttons and background
UI_BUTTON_COLOR = (150, 150, 150)
UI_BACKGROUND_COLOR = (200, 200, 200)

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40


class UI:
    def __init__(
        self,
        screen_width,
        screen_height,
        ui_area_width_ratio=0.25,
        ui_button_color=(255, 255, 255),
        ui_background_color=(0, 0, 0),
    ):
        self.UI_AREA_WIDTH = int(screen_width * ui_area_width_ratio)
        self.UI_AREA_HEIGHT = screen_height
        self.UI_AREA_X = screen_width - self.UI_AREA_WIDTH
        self.UI_AREA_Y = 0
        self.UI_BUTTON_COLOR = ui_button_color
        self.UI_BACKGROUND_COLOR = ui_background_color
        self.settings_button = Button(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 10,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Settings",
            button_color=self.UI_BUTTON_COLOR,
        )
        self.pause_button = Button(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 70,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Pause",
            button_color=self.UI_BUTTON_COLOR,
        )
        self.ui_exit_button = Button(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 130,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Exit",
            button_color=self.UI_BUTTON_COLOR,
        )

    def resize(self, screen_width, screen_height, ui_area_width_ratio=0.25):
        self.UI_AREA_WIDTH = int(screen_width * ui_area_width_ratio)
        self.UI_AREA_HEIGHT = screen_height
        self.UI_AREA_X = screen_width - self.UI_AREA_WIDTH


def game_loop(game_map, game_clock, screen):
    # Create the UI buttons
    ui = UI(
        GameSettings.SCREEN_WIDTH,
        GameSettings.SCREEN_HEIGHT,
        ui_button_color=UI_BUTTON_COLOR,
        ui_background_color=UI_BACKGROUND_COLOR,
    )

    running = True
    while running:
        dt = game_clock.tick(FPS) / 1000.0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ui.ui_exit_button.is_clicked(event.pos):
                    GameSettings.MENU_STATE = "menu"
                    running = False

        # Update the game state
        game_map.update(dt)

        draw_game(screen, game_map, ui)

        # Update the display
        pygame.display.flip()

        # Tick the game clock
        game_clock.tick(FPS)


def draw_game(screen, game_map, ui):
    screen.fill((0, 0, 0))  # Clear the screen with black

    game_map.draw(screen)

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
    ui.settings_button.draw(screen)
    ui.pause_button.draw(screen)
    ui.ui_exit_button.draw(screen)

    # Update the display
    pygame.display.update()
