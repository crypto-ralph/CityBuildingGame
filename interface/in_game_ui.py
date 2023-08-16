import pygame

from button import SpriteButton
from interface.button_factory import create_hut_button, create_ui_exit_button, create_road_button, create_church_button

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40


class UI:
    def __init__(
            self,
            screen_width,
            screen_height,
            asset_manager,
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
            font_size=15,
            button_color=self.UI_BUTTON_COLOR,
        )
        self.pause_button = SpriteButton(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 70,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Pause",
            font_size=15,
            button_color=self.UI_BUTTON_COLOR,
        )
        self.ui_exit_button = create_ui_exit_button(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 130,
        )
        self.hut_button = create_hut_button(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 190,
            image=asset_manager.get_asset("hut")
        )

        self.church_button = create_church_button(
            self.UI_AREA_X + 100,
            self.UI_AREA_Y + 190,
            image=asset_manager.get_asset("church")
        )

        self.road_button = create_road_button(
            self.UI_AREA_X + 10,
            self.UI_AREA_Y + 270,
        )

        self.TOP_BAR_HEIGHT = 30
        self.money = 0
        self.income = 0
        self.citizens = 0

        self.buttons.add(self.settings_button)
        self.buttons.add(self.pause_button)
        self.buttons.add(self.ui_exit_button)
        self.buttons.add(self.hut_button)
        self.buttons.add(self.church_button)
        self.buttons.add(self.road_button)

    def resize(self, screen_width, screen_height, ui_area_width_ratio=0.25):
        self.UI_AREA_WIDTH = int(screen_width * ui_area_width_ratio)
        self.UI_AREA_HEIGHT = screen_height
        self.UI_AREA_X = screen_width - self.UI_AREA_WIDTH

    def draw_top_bar(self, screen):
        font = pygame.font.SysFont("Verdana", 15)
        text_color = (223, 168, 120)
        money_text = font.render(f"Money: {self.money}", True, text_color)

        if int(self.income) < 0:
            sign = ""
            income_color = (239, 98, 98)
        elif int(self.income) > 0:
            sign = "+"
            income_color = (85, 122, 70)
        else:
            sign = ""
            income_color = (223, 168, 120)

        income_text = font.render(f"Income: {sign}{self.income}", True, income_color)
        citizens_text = font.render(f"Citizens: {self.citizens}", True, text_color)

        pygame.draw.rect(screen, (108, 52, 40), (0, 0, self.UI_AREA_X, self.TOP_BAR_HEIGHT))
        screen.blit(money_text, (10, 5))
        screen.blit(income_text, (200, 5))
        screen.blit(citizens_text, (400, 5))

    def draw_buttons_background(self, screen):
        pygame.draw.rect(
            screen,
            self.UI_BACKGROUND_COLOR,
            (self.UI_AREA_X, 0, self.UI_AREA_WIDTH, self.UI_AREA_HEIGHT),
        )

    @staticmethod
    def draw_info_box(info_box, screen, line_spacing=10):
        # Create the text surface
        position = info_box['position']
        lines = info_box['text'].split('\n')
        text_surface = info_box['font'].render(info_box['text'], True, info_box['text_color'])
        y = position[1]  # initialize y coordinate
        pygame.draw.rect(screen, info_box['background_color'], (*position, *info_box['size']))

        # Calculate the position of the text surface within the info box
        # text_rect = text_surface.get_rect(center=(position[0], position[1]))
        if len(lines) > 0:
            for line in lines:
                # render each line individually
                text_surface = info_box['font'].render(line, True, info_box['text_color'])
                text_rect = text_surface.get_rect(topleft=(position[0] + 8, y + text_surface.get_height() / 2))
                screen.blit(text_surface, text_rect)
                y += text_surface.get_height() + line_spacing  # move y coordinate for the next line

    def draw(self, surface):
        self.draw_top_bar(surface)
        self.draw_buttons_background(surface)
        self.buttons.draw(surface)
