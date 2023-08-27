import pygame

from geometry import Size
from interface.button import SpriteButton
from interface.button_factory import create_hut_button, create_road_button, create_church_button


class UI:
    BACKGROUND_COLOR = (200, 200, 200)
    TEXT_FONT = "Verdana"

    def __init__(
        self,
        screen_size: Size,
        asset_manager,
        ui_area_width_ratio=0.25,
    ):
        self.ui_area_width = int(screen_size.width * ui_area_width_ratio)
        self.ui_area_height = screen_size.height
        self.ui_area_x = screen_size.width - self.ui_area_width
        self.ui_area_y = 0

        self.building_buttons = pygame.sprite.Group()
        self.control_buttons = pygame.sprite.Group()

        self.top_bar_font = pygame.font.SysFont(self.TEXT_FONT, 15)
        self.building_header_font = pygame.font.SysFont(self.TEXT_FONT, 18)

        self.control_button_size = 60
        total_button_width = 2 * self.control_button_size
        start_x = (self.ui_area_width - total_button_width) / 2
        self.control_button_y = 10

        pause_img = asset_manager.load_and_scale("pause_btn", (self.control_button_size, self.control_button_size))
        settings_img = asset_manager.load_and_scale(
            "settings_btn", (self.control_button_size, self.control_button_size)
        )

        pause_hover_img = asset_manager.load_and_scale(
            "pause_hover_btn", (self.control_button_size, self.control_button_size)
        )
        settings_hover_img = asset_manager.load_and_scale(
            "settings_hover_btn", (self.control_button_size, self.control_button_size)
        )

        self.pause_button = SpriteButton(
            self.ui_area_x + start_x,
            self.ui_area_y + self.control_button_y,
            button_color=self.BACKGROUND_COLOR,
            asset_image=pause_img,
            hover_asset_image=pause_hover_img,
        )

        self.settings_button = SpriteButton(
            self.ui_area_x + start_x + self.control_button_size,
            self.ui_area_y + self.control_button_y,
            button_color=self.BACKGROUND_COLOR,
            asset_image=settings_img,
            hover_asset_image=settings_hover_img,
        )

        self.hut_button = create_hut_button(
            self.ui_area_x + 10, self.ui_area_y + 160, image=asset_manager.get_asset("hut")
        )
        self.church_button = create_church_button(
            self.ui_area_x + 100,
            self.ui_area_y + 160,
            image=asset_manager.load_and_scale("church", Size(72, 72).as_tuple()),
        )
        self.road_button = create_road_button(self.ui_area_x + 10, self.ui_area_y + 250)

        self.top_bar_height = 30

        self.control_buttons.add(self.settings_button)
        self.control_buttons.add(self.pause_button)
        self.building_buttons.add(self.hut_button)
        self.building_buttons.add(self.church_button)
        self.building_buttons.add(self.road_button)

    def resize(self, screen_width, screen_height, ui_area_width_ratio=0.25):
        self.ui_area_width = int(screen_width * ui_area_width_ratio)
        self.ui_area_height = screen_height
        self.ui_area_x = screen_width - self.ui_area_width

    def draw_top_bar(self, screen, money: int, income: int, citizens: int):
        text_color = (223, 168, 120)
        money_text = self.top_bar_font.render(f"Money: {money}", True, text_color)

        sign = "+" if income > 0 else ""
        income_color = (85, 122, 70) if income > 0 else (239, 98, 98) if income < 0 else (223, 168, 120)

        income_text = self.top_bar_font.render(f"Income: {sign}{income}", True, income_color)
        citizens_text = self.top_bar_font.render(f"Citizens: {citizens}", True, text_color)

        pygame.draw.rect(screen, (108, 52, 40), (0, 0, self.ui_area_x, self.top_bar_height))

        # Calculate the x and y coordinates to center-align the text
        money_x = (
            self.ui_area_x // 6 - money_text.get_width() // 2
        )  # Divided by 6 to place in the center of the first section
        money_y = (self.top_bar_height - money_text.get_height()) // 2

        income_x = self.ui_area_x // 2 - income_text.get_width() // 2  # Center of the screen
        income_y = (self.top_bar_height - income_text.get_height()) // 2

        citizens_x = 5 * self.ui_area_x // 6 - citizens_text.get_width() // 2  # Center of the third section
        citizens_y = (self.top_bar_height - citizens_text.get_height()) // 2

        # Draw the text onto the screen at the calculated coordinates
        screen.blit(money_text, (money_x, money_y))
        screen.blit(income_text, (income_x, income_y))
        screen.blit(citizens_text, (citizens_x, citizens_y))

    def draw_buttons_background(self, screen):
        pygame.draw.rect(
            screen,
            self.BACKGROUND_COLOR,
            (self.ui_area_x, 0, self.ui_area_width, self.ui_area_height),
        )

    def draw_section_text(self, screen):
        text_surface = self.building_header_font.render("--Buildings--", True, (0, 0, 0))
        surface_width = text_surface.get_width()

        screen.blit(
            text_surface,
            [
                self.ui_area_x + (self.ui_area_width - surface_width) / 2,
                self.ui_area_y + self.control_button_y + self.control_button_size + 50,
            ],
        )

    def draw(self, surface, money, income, citizens):
        self.draw_top_bar(surface, money, income, citizens)
        self.draw_buttons_background(surface)
        self.draw_section_text(surface)
        self.building_buttons.draw(surface)
        self.control_buttons.draw(surface)
