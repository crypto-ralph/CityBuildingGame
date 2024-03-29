import pygame

from game_settings import GameSettings


class InfoBox:
    def __init__(self, text, font_name, font_size, text_color, background_color, size, position):
        self.text = text
        self.font = pygame.font.SysFont(
            font_name, font_size
        )  # Creating font object using the provided font_name and font_size
        self.text_color = text_color
        self.background_color = background_color
        self.size = size
        self.position = position

    def draw(self, screen, line_spacing=10):
        # Check if the InfoBox will be outside the screen area
        if self.position[0] + self.size[0] > GameSettings.SCREEN_WIDTH:
            # Flip the position of the InfoBox
            # Assuming that you have access to the button's x-coordinate here.
            # Replace `button_x` with the actual x-coordinate.
            self.position = (self.position[0] - self.size[0], self.position[1])
        # Create the text surface
        position = self.position
        lines = self.text.split("\n")
        y = position[1]  # initialize y coordinate

        pygame.draw.rect(screen, self.background_color, (*position, *self.size))

        # Calculate the position of the text surface within the info box
        if len(lines) > 0:
            for line in lines:
                # render each line individually
                text_surface = self.font.render(line, True, self.text_color)
                text_rect = text_surface.get_rect(topleft=(position[0] + 8, y + text_surface.get_height() / 2))
                screen.blit(text_surface, text_rect)
                y += text_surface.get_height() + line_spacing  # move y coordinate for the next line
