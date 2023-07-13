import sys

import pygame
from button import SpriteButton
from game_settings import GameSettings

UI_BUTTON_COLOR = (150, 150, 150)
HOVER_BUTTON_COLOR = (200, 200, 200)
BUTTON_PADDING = 20
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Create the version and build number text
pygame.font.init()
version_text = f"Version: 1.0"
build_text = f"Build: 2022-03-06"
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
    start_button = SpriteButton(
        x=50,
        y=50,
        width=200,
        height=50,
        text="Start Game",
        button_color=UI_BUTTON_COLOR,
        hover_color=HOVER_BUTTON_COLOR,
    )
    settings_button = SpriteButton(
        x=50, y=120, width=200, height=50, text="Settings", button_color=UI_BUTTON_COLOR, hover_color=HOVER_BUTTON_COLOR,
    )
    exit_button = SpriteButton(
        x=50,
        y=190,
        width=200,
        height=50,
        text="Exit Game",
        button_color=UI_BUTTON_COLOR,
        hover_color=HOVER_BUTTON_COLOR,
    )
    credits_button = SpriteButton(
        x=50, y=260, width=200, height=50, text="Credits", button_color=UI_BUTTON_COLOR, hover_color=HOVER_BUTTON_COLOR,
    )
    menu_buttons = pygame.sprite.Group()
    menu_buttons.add(start_button)
    menu_buttons.add(settings_button)
    menu_buttons.add(exit_button)
    menu_buttons.add(credits_button)

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
                        # Open the settings window
                        settings_menu_loop(screen)
                    elif exit_button.is_clicked(event.pos):
                        GameSettings.MENU_STATE = "exit_game"
                        running = False
                    elif credits_button.is_clicked(event.pos):
                        print("Credits button clicked")

        for button in menu_buttons:
            button.handle_hovered(pygame.mouse.get_pos())


        # Draw the screen
        screen.fill((0, 0, 0))
        menu_buttons.draw(screen)
        screen.blit(version_surface, version_rect)
        screen.blit(build_surface, build_rect)
        pygame.display.flip()


def settings_menu_loop(screen):
    resolutions = [(640, 480), (800, 600), (1024, 768), (1280, 720), (1920, 1080)]
    buttons = pygame.sprite.Group()
    for i, resolution in enumerate(resolutions):
        x = GameSettings.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        y = BUTTON_PADDING + i * (BUTTON_HEIGHT + BUTTON_PADDING)
        text = f"{resolution[0]}x{resolution[1]}"
        button = SpriteButton(
            x, y, BUTTON_WIDTH, BUTTON_HEIGHT, text=text, button_color=UI_BUTTON_COLOR, hover_color=HOVER_BUTTON_COLOR,
        )
        buttons.add(button)

    back_button = SpriteButton(
        x=GameSettings.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
        y=GameSettings.SCREEN_HEIGHT - 2 * BUTTON_PADDING - BUTTON_HEIGHT,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        text="Back to menu",
        button_color=UI_BUTTON_COLOR,
        hover_color=HOVER_BUTTON_COLOR,
    )
    buttons.add(back_button)

    # Function to update button positions based on the current resolution
    def update_button_positions():
        for i, button in enumerate(buttons):
            button.rect.x = GameSettings.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
            button.rect.y = BUTTON_PADDING + i * (BUTTON_HEIGHT + BUTTON_PADDING)

        back_button.rect.x = GameSettings.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        back_button.rect.y = GameSettings.SCREEN_HEIGHT - 2 * BUTTON_PADDING - BUTTON_HEIGHT

    # Update button positions initially
    update_button_positions()

    # Highlight the button for the current resolution
    current_resolution = (GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)
    for button in buttons:
        if button.text == f"{current_resolution[0]}x{current_resolution[1]}":
            button.color = (180, 180, 180)

    running = True
    while running:
        for button in buttons:
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
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button.text == "Back to menu":
                                running = False
                                continue
                            # Set the resolution and update the screen
                            current_resolution = tuple(map(int, button.text.split("x")))
                            GameSettings.set_screen_dimensions(
                                current_resolution[0], current_resolution[1]
                            )
                            screen = pygame.display.set_mode(current_resolution)

                            # Update button positions based on the new resolution
                            update_button_positions()

        # Draw the screen
        screen.fill((0, 0, 0))
        buttons.draw(screen)
        pygame.display.flip()
