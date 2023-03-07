import sys

import pygame

from game_loop import game_loop
from game_settings import GameSettings
from main_menu import main_menu
from map import GameMap, MAP_WIDTH, MAP_HEIGHT

pygame.init()

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
pygame.display.set_caption("City Building Game")

# Set up the game clock
clock = pygame.time.Clock()

# Define the main loop
running = True

while running:
    if GameSettings.MENU_STATE == "menu":
        # Run the main menu
        main_menu(screen)
    elif GameSettings.MENU_STATE == "game":
        game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
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

# Give credit where credit is due
print("Credits: This game was created with the help of ChatGPT, a large language model trained by OpenAI.")
