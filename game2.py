import pygame
import numpy as np

pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isometric View")

# Define the colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the tile size
TILE_WIDTH = 64
TILE_HEIGHT = 32

# Define the map size
MAP_WIDTH = 10
MAP_HEIGHT = 10

# Define the tiles
tiles = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=int)

# Define the images
tile_images = {
    0: pygame.image.load("grass.png").convert_alpha(),
    1: pygame.image.load("water.png").convert_alpha(),
}

# Define the camera position
camera_x = 0
camera_y = 0

# Define the main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                camera_y -= TILE_HEIGHT // 2
            elif event.key == pygame.K_DOWN:
                camera_y += TILE_HEIGHT // 2
            elif event.key == pygame.K_LEFT:
                camera_x -= TILE_WIDTH // 2
            elif event.key == pygame.K_RIGHT:
                camera_x += TILE_WIDTH // 2

    # Clear the screen
    screen.fill(WHITE)

    # Draw the tiles
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            tile_type = tiles[x, y]
            tile_image = tile_images[tile_type]

            # Calculate the screen coordinates of the tile
            screen_x = (x - y) * TILE_WIDTH // 2 + WIDTH // 2 - TILE_WIDTH // 2 + camera_x
            screen_y = (x + y) * TILE_HEIGHT // 2 + TILE_HEIGHT // 2 + camera_y

            # Draw the tile
            screen.blit(tile_image, (screen_x, screen_y))

    # Update the screen
    pygame.display.flip()

# Clean up
pygame.quit()