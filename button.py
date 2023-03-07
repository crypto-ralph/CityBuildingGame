import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font_size=20,
        text_color=(255, 255, 255),
        button_color=(0, 0, 0),
    ):
        pygame.font.init()
        self.rect = pygame.Rect(x, y, width, height)
        self.button_color = button_color
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
