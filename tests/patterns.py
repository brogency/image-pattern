from __future__ import annotations
from os.path import join
from typing import Tuple
from pathlib import Path
from typing import (
    List,
    Optional,
)
from image_pattern import (
    Pattern,
    Canvas,
    Rectangle,
    Point,
    Layer,
    Text,
    HorizontalAlignment,
    VerticalAlignment,
    Position,
    Context,
)

from .settings import ASSETS_PATH


class ComplexContext(Context):
    right_image: Path
    left_image: Path
    title: str
    text: Optional[str]
    layer_exists: bool


class ComplexPattern(Pattern):
    canvas: Canvas = Canvas(
        size=(1200, 630),
    )
    layers: List[Layer] = [
        Layer(
            Rectangle(
                background_color=(65, 209, 46),
                size=(1200, 630),
                point=Point(
                    x=0,
                    y=0,
                ),
            ),
        ),
        Layer(
            Rectangle(
                background_image=ComplexContext.var('left_image'),
                size=(458, 630),
                point=Point(
                    x=458,
                    y=0,
                ),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                brightness=0.8,
            ),
            Rectangle(
                background_image=ComplexContext.var('right_image'),
                size=(458, 630),
                point=Point(
                    x=742,
                    y=0,
                ),
                brightness=0.8,
            ),
        ),
        Layer(
            Text(
                text=ComplexContext.var('title'),
                font=join(ASSETS_PATH, 'IBMPlexSans-Bold.ttf'),
                font_size=54,
                point=Point(
                    x=58,
                    y=68,
                ),
                margin=Position(
                    right=516,
                )
            ),
            Text(
                text=ComplexContext.var('text'),
                font=join(ASSETS_PATH, 'IBMPlexSans-Regular.ttf'),
                font_size=32,
                point=Point(
                    x=58,
                    y=152,
                ),
                margin=Position(
                    right=516,
                )
            ),
        ),
        Layer(
            Text(
                text='This is adventure time!!!',
                font=join(ASSETS_PATH, 'IBMPlexSans-Bold.ttf'),
                font_size=32,
                point=Point(
                    x=58,
                    y=538,
                ),
            ),
        ),
        Layer(
            Text(
                text='FINN THE HUMAN',
                font=join(ASSETS_PATH, 'IBMPlexSans-Regular.ttf'),
                font_size=32,
                font_color=(202, 202, 202),
                point=Point(
                    x=684,
                    y=538,
                ),
                horizontal_alignment=HorizontalAlignment.RIGHT,
            ),
        ),
        Layer(
            Rectangle(
                point=Point(x=0, y=0),
                background_color=(255, 0, 0),
                size=(1200, 30),
                alpha=200,
            ),
            exist=lambda context=None: context.layer_exists if context else True,
        ),
        Layer(
            Text(
                text='FINN THE HUMAN',
                font=join(ASSETS_PATH, 'IBMPlexSans-Regular.ttf'),
                font_size=64,
                font_color=(255, 255, 255),
                point=Point(
                    x=600,
                    y=315,
                ),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            )
        ),
    ]


class SimpleTestPattern(Pattern):
    canvas: Canvas = Canvas(
        size=(1200, 720),
    )
    layers: List[Layer] = [
        Layer(
            Rectangle(
                background_color=(153, 102, 255),
                size=(600, 720),
                point=Point(
                    x=0,
                    y=0,
                ),
            ),
            Rectangle(
                background_color=(153, 255, 102),
                size=(600, 720),
                point=Point(
                    x=600,
                    y=0,
                ),
            ),
        ),
        Layer(
            Text(
                text='SIMPLE',
                font=join(ASSETS_PATH, 'IBMPlexSans-Regular.ttf'),
                font_size=300,
                font_color=(255, 255, 255),
                point=Point(
                    x=600,
                    y=360,
                ),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
    ]


class SmallTestPatternContext(Context):
    text: str
    background_color: Tuple[int, int, int]
    horizontal_alignment: HorizontalAlignment
    vertical_alignment: VerticalAlignment


class SmallTestPattern(Pattern):
    canvas: Canvas = Canvas(
        size=(500, 500),
    )
    layers: List[Layer] = [
        Layer(
            Rectangle(
                background_color=SmallTestPatternContext.var('background_color'),
                size=(500, 500),
                point=Point(
                    x=0,
                    y=0,
                ),
            ),
        ),
        Layer(
            Text(
                text=SmallTestPatternContext.var('text'),
                font=join(ASSETS_PATH, 'IBMPlexSans-Regular.ttf'),
                font_size=300,
                font_color=(255, 255, 255),
                point=Point(
                    x=250,
                    y=250,
                ),
                horizontal_alignment=SmallTestPatternContext.var('horizontal_alignment'),
                vertical_alignment=SmallTestPatternContext.var('vertical_alignment'),
            ),
        ),
    ]


class OffsetPattern(Pattern):
    canvas = Canvas(
        size=(1200, 720),
    )
    layers: List[Layer] = [
        Layer(
            Rectangle(
                background_image=join(ASSETS_PATH, 'Finn-the-human.jpg'),
                size=(1200, 720),
                point=Point(
                    x=0,
                    y=0,
                ),
            ),
        ),
        Layer(
            Text(
                text='Text text',
                font=join(ASSETS_PATH, 'IBMPlexSans-Regular.ttf'),
                font_size=100,
                font_color=(255, 255, 255),
                point=Point(
                    x=0,
                    y=0,
                ),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.TOP,
            ),
            Text(
                text='Text text',
                font=join(ASSETS_PATH, 'IBMPlexSans-Regular.ttf'),
                font_size=100,
                font_color=(255, 255, 255),
                point=Point(
                    x=0,
                    y=-30,
                ),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.TOP,
            )
        ),
    ]
