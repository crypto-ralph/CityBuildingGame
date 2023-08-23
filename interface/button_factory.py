from building import Church, House, Road
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
    info_box = InfoBox(
        text=f"{Church.name}\nCost: {Church.cost}\n",
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
