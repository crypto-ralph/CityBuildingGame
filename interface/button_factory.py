from building import House
from button import ButtonWithInfoBox, SpriteButton


def create_hut_button(x: int, y: int, image) -> ButtonWithInfoBox:
    return ButtonWithInfoBox(
        x=x,
        y=y,
        width=100,
        height=40,
        text=House.name,
        image=image,
        border=True,
        border_color=(108, 52, 40),
        border_width=2,
        button_color=(255, 255, 255),
        info_box_background_color=(108, 52, 40),
        info_box_text_color=(223, 168, 120),
        info_box_font_size=13,
        info_box_text=f"{House.name}\nCost: {House.cost}\nIncome: {House.income}\nCitizens: {House.citizens}",
        info_box_font_name="Verdana",
        info_box_size=(100, 120),
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
    return ButtonWithInfoBox(
        x=x,
        y=y,
        width=72,
        height=72,
        text="Road",
        button_color=(150, 150, 150)
    )

