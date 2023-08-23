from interface.button import SpriteButton, ButtonWithInfoBox
from interface.info_box import InfoBox


class ButtonBuilder:
    def __init__(self):
        # Default values for the Button properties
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 40
        self.text = ""
        self.text_color = (0, 0, 0)
        self.font_name = "Arial"
        self.font_size = 20
        self.button_color = (255, 255, 255)
        self.border = False
        self.border_color = (0, 0, 0)
        self.border_width = 1
        self.image = None
        self.hover_color = (100, 100, 100)

        # Default values for InfoBox
        self.info_box: InfoBox = None

    # Button configuration methods
    def position(self, x, y):
        self.x = x
        self.y = y
        return self

    def size(self, width, height):
        self.width = width
        self.height = height
        return self

    def with_text(self, text, font_name="Arial", font_size=20, text_color=(0, 0, 0)):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        return self

    def with_colors(self, button_color, hover_color=(100, 100, 100)):
        self.button_color = button_color
        self.hover_color = hover_color
        return self

    def with_border(self, border_color, border_width=1):
        self.border = True
        self.border_color = border_color
        self.border_width = border_width
        return self

    def with_image(self, image):
        self.image = image
        return self

    # InfoBox configuration methods
    def with_info_box(
        self,
        text,
        font_name="Verdana",
        font_size=13,
        text_color=(223, 168, 120),
        background_color=(108, 52, 40),
        size=(100, 120),
        position=None,
    ):
        if position is None:
            position = (self.x + self.width - 20, self.y + self.height)
        self.info_box = InfoBox(
            text=text,
            font_name=font_name,
            font_size=font_size,
            text_color=text_color,
            background_color=background_color,
            size=size,
            position=position,
        )
        return self

    def attach_info_box(self, info_box: InfoBox):
        """
        Attach an externally generated InfoBox to the button.
        """
        self.info_box = info_box
        return self

    # Button creation method
    def build(self):
        if self.info_box:
            return ButtonWithInfoBox(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                text=self.text,
                text_color=self.text_color,
                button_color=self.button_color,
                font_name=self.font_name,
                font_size=self.font_size,
                image=self.image,
                hover_color=self.hover_color,
                border=self.border,
                border_color=self.border_color,
                border_width=self.border_width,
                info_box=self.info_box,
            )
        else:
            return SpriteButton(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                text=self.text,
                text_color=self.text_color,
                button_color=self.button_color,
                font_name=self.font_name,
                font_size=self.font_size,
                asset_image=self.image,
                hover_color=self.hover_color,
                border=self.border,
                border_color=self.border_color,
                border_width=self.border_width,
            )

    # Reset the builder for next usage (optional)
    def reset(self):
        self.__init__()
