from __future__ import annotations
from typing import List
from django.contrib.staticfiles import finders
from image_pattern import (
    Pattern,
    Context,
    Canvas,
    Rectangle,
    Text,
    Layer,
    Point,
    VerticalAlignment,
    HorizontalAlignment,
)


class ImageContext(Context):
    text: str


class ImagePattern(Pattern):
    canvas = Canvas(
        size=(500, 500)
    )
    layers: List[Layer] = [
        Layer(
            Rectangle(
                background_color=(81, 98, 224),
                size=(500, 500),
                point=Point(x=0, y=0),
            ),
        ),
        Layer(
            Text(
                point=Point(x=250, y=250),
                text=ImageContext.var('text'),
                font=finders.find('OpenSans-Bold.ttf'),
                font_size=150,
                font_color=(255, 255, 255),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),

    ]
