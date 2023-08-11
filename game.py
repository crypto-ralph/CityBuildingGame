import sys

import pygame

from game_loop import game_loop
from game_settings import GameSettings
from menu_loop import main_menu, settings_menu
from map import Map, MAP_WIDTH, MAP_HEIGHT

pygame.init()

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode(
    (GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)
)
pygame.display.set_caption("City Building Game")

# Set up the game clock
clock = pygame.time.Clock()

# Define the main loop
running = True

while running:
    if GameSettings.MENU_STATE == "menu":
        # Run the main menu
        main_menu(screen)
    elif GameSettings.MENU_STATE == "settings":
        settings_menu(screen)
    elif GameSettings.MENU_STATE == "game":
        game_map = Map(MAP_WIDTH, MAP_HEIGHT)
        game_clock = pygame.time.Clock()
        game_loop(game_map, game_clock, screen)
    elif GameSettings.MENU_STATE == "exit_game":
        pygame.quit()
        sys.exit()
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
