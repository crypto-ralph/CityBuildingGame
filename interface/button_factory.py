from building import Church, House, Road
from game_settings import GameSettings
from interface.button_builder import ButtonBuilder
from interface.info_box import InfoBox

"""
UI Buttons
"""


def create_hut_button(x: int, y: int, image):
    info_box = InfoBox(
        text=f"{House.name}\nCost: {House.cost}\nIncome: {House.income}\nCitizens: {House.citizens}",
        font_name="Verdana",
        font_size=13,
        text_color=(223, 168, 120),
        background_color=(108, 52, 40),
        size=(100, 120),
        position=(x + 100 - 20, y + 40),
    )

    button = (
        ButtonBuilder()
        .position(x, y)
        .with_image(image)
        .with_border((108, 52, 40), 2)
        .with_colors(button_color=(255, 255, 255))
        .attach_info_box(info_box)
        .build()
    )
    return button


def create_church_button(x: int, y: int, image):
    info_box_width = 100
    info_box_height = 80
    info_box_x = x + 100 - 20
    info_box_y = y + 40

    # # Check if the InfoBox will be outside of the screen area
    # if info_box_x + info_box_width > GameSettings.SCREEN_WIDTH:
    #     # Flip the position of the InfoBox vertically
    #     info_box_x = x - info_box_width + 20

    info_box = InfoBox(
        text=f"{Church.name}\nCost: {Church.cost}\nIncome: {Church.income}",
        font_name="Verdana",
        font_size=13,
        text_color=(223, 168, 120),
        background_color=(108, 52, 40),
        size=(info_box_width, info_box_height),
        position=(info_box_x, info_box_y),
    )

    button = (
        ButtonBuilder()
        .position(x, y)
        .with_image(image)
        .with_border((108, 52, 40), 2)
        .with_colors(button_color=(255, 255, 255))
        .attach_info_box(info_box)
        .build()
    )
    return button


def create_road_button(x: int, y: int):
    info_box = InfoBox(
        text=f"{Road.type}\nCost: {Road.cost}\nIncome:",
        font_name="Verdana",
        font_size=13,
        text_color=(223, 168, 120),
        background_color=(108, 52, 40),
        size=(100, 120),
        position=(x + 100 - 20, y + 40),
    )
    button = (
        ButtonBuilder()
        .position(x, y)
        .size(72, 72)
        .with_text(text=Road.type, font_name="Verdana", font_size=16)
        .with_colors(button_color=(150, 150, 150))
        .attach_info_box(info_box)
        .build()
    )
    return button
