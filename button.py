from abc import ABC

import pygame


class Button(ABC):
    def __init__(self, x, y, width, height, text, text_color, font_name, font_size,
                 button_color, hover_color):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.button_color = button_color
        self.hover_color = hover_color
        self.hovered = False

    def is_clicked(self, pos):
        """
        Checks if the button is clicked given a position.

        :param pos: A tuple containing the x and y coordinates of the click position.
        :type pos: tuple
        :return: True if the button is clicked, False otherwise.
        :rtype: bool
        """
        return self.rect.collidepoint(pos)


class SpriteButton(Button, pygame.sprite.Sprite):
    """A button class that inherits from Button and pygame.sprite.Sprite."""

    def __init__(self, x, y, width, height, text,
                 text_color=(0, 0, 0),
                 button_color=(0, 0, 0),
                 font_name="Arial",
                 font_size=20,
                 image=None,
                 hover_color=(100, 100, 100)):
        Button.__init__(self, x, y, width, height, text, text_color=text_color, font_name=font_name,
                        font_size=font_size, button_color=button_color, hover_color=hover_color)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(self.button_color)
        if image is not None:
            self.image.blit(image, (0, 0))
        self.draw_text()

    def draw_text(self):
        """Draws the button text on the specified surface."""
        text_surface = self.font.render(self.text, True, self.text_color)
        surface_width = text_surface.get_width()
        surface_height = text_surface.get_height()
        self.image.blit(text_surface, [self.width / 2 - surface_width / 2, self.height / 2 - surface_height / 2])

    def handle_hovered(self, pos):
        if self.is_clicked(pos) and not self.hovered:
            self.hovered = True
            self.image.fill(self.hover_color)
            self.draw_text()
        elif not self.is_clicked(pos) and self.hovered:
            self.hovered = False
            self.image.fill(self.button_color)
            self.draw_text()

    def set_color(self, color):
        if color != self.button_color:
            self.button_color = color
            self.image.fill(color)
            self.draw_text()



