from building import House
from button import ButtonWithInfoBox, SpriteButton


def create_hut_button(x: int, y: int) -> ButtonWithInfoBox:
    return ButtonWithInfoBox(
        x=x,
        y=y,
        width=100,
        height=40,
        text=House.name,
        button_color=(255, 255, 255),
        info_box_background_color=(108, 52, 40),
        info_box_text_color=(223, 168, 120),
        info_box_font_size=13,
        info_box_text=f"{House.name}\nIncome: {House.income}\nCitizens: {House.citizens}",
        info_box_font_name="Verdana",
        info_box_size=(100, 100),
        info_box_position=(x + 100 - 20, y + 40),
    )


def create_ui_exit_button(x: int, y: int) -> SpriteButton:
    return SpriteButton(
        x=x,
        y=y,
        width=100,
        height=40,
        text="Exit",
        button_color=(150, 150, 150)
    )


def create_road_button(x: int, y: int) -> SpriteButton:
    return SpriteButton(
        x=x,
        y=y,
        width=100,
        height=40,
        text="Road",
        button_color=(150, 150, 150)
    )

