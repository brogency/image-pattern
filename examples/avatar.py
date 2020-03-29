from __future__ import annotations
from os.path import (
    abspath,
    join,
)
from pathlib import Path
from typing import List
from image_pattern import (
    Pattern,
    Canvas,
    Layer,
    Rectangle,
    Point,
    Text,
    Position,
    HorizontalAlignment,
    VerticalAlignment,
    Context,
)

BASE_DIR = Path(abspath(__file__)).parent.parent
FONT_PATH = join(BASE_DIR, 'assets/IBMPlexSans-Bold.ttf')


class AvatarContext(Context):
    first_char: str
    second_char: str


class Avatar(Pattern):
    canvas = Canvas(
        size=(200, 200),
    )
    layers: List[Layer] = [
        Layer(
            Rectangle(
                size=(100, 200),
                point=Point(x=0, y=0),
                background_color=(51, 204, 255),
            ),
            Rectangle(
                size=(100, 200),
                point=Point(x=100, y=0),
                background_color=(255, 51, 153),
            ),
        ),
        Layer(
            Text(
                text=AvatarContext.var('first_char'),
                font=FONT_PATH,
                font_color=(255, 255, 255),
                font_size=102,
                point=Point(x=50, y=100),
                margin=Position(
                    left=20,
                    right=20,
                ),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
            Text(
                text=AvatarContext.var('second_char'),
                font=FONT_PATH,
                font_color=(255, 255, 255),
                font_size=102,
                point=Point(x=150, y=100),
                margin=Position(
                    left=20,
                    right=20,
                ),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
    ]


context = AvatarContext(
    first_char='I',
    second_char='P',
)
avatar_pattern = Avatar(context=context)
image = avatar_pattern.render()
image.save('avatar.jpg', 'JPEG')
