import pygame

from button import SpriteButton

# Define the colors for the UI buttons and background


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
        self.buttons = pygame.sprite.Group()
        self.settings_button = SpriteButton(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 10,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Settings",
            button_color=self.UI_BUTTON_COLOR,
        )
        self.pause_button = SpriteButton(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 70,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Pause",
            button_color=self.UI_BUTTON_COLOR,
        )
        self.ui_exit_button = SpriteButton(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 130,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Exit",
            button_color=self.UI_BUTTON_COLOR,
        )

        self.hut_button = SpriteButton(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 190,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Hut",
            button_color=self.UI_BUTTON_COLOR,
        )

        self.TOP_BAR_HEIGHT = 30
        self.money = 0
        self.income = 0
        self.citizens = 0

        self.buttons.add(self.settings_button)
        self.buttons.add(self.pause_button)
        self.buttons.add(self.ui_exit_button)
        self.buttons.add(self.hut_button)

    def resize(self, screen_width, screen_height, ui_area_width_ratio=0.25):
        self.UI_AREA_WIDTH = int(screen_width * ui_area_width_ratio)
        self.UI_AREA_HEIGHT = screen_height
        self.UI_AREA_X = screen_width - self.UI_AREA_WIDTH

    def draw(self, surface):
        self.draw_top_bar(surface)
        self.draw_buttons_background(surface)
        self.buttons.draw(surface)

    def draw_top_bar(self, screen):
        font = pygame.font.SysFont("Arial", 20)
        money_text = font.render(f"Money: {self.money}", True, (0, 0, 0))
        sign = "+"
        if int(self.income) < 0:
            sign = "-"

        income_text = font.render(f"Income: {sign}{self.income}", True, (0, 0, 0))
        citizens_text = font.render(f"Citizens: {self.citizens}", True, (0, 0, 0))

        pygame.draw.rect(screen, (139, 69, 19), (0, 0, self.UI_AREA_X, self.TOP_BAR_HEIGHT))
        screen.blit(money_text, (10, 5))
        screen.blit(income_text, (200, 5))
        screen.blit(citizens_text, (400, 5))

    def draw_buttons_background(self, screen):
        # Draw the UI buttons
        pygame.draw.rect(
            screen,
            self.UI_BACKGROUND_COLOR,
            (screen.get_height(), 0, self.UI_AREA_WIDTH, self.UI_AREA_HEIGHT),
        )
