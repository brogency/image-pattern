from os.path import (
    join,
    dirname,
)
from pathlib import Path
from typing import List
from image_pattern import (
    __version__,
    Pattern,
    Canvas,
    Rectangle,
    Point,
    Layer,
    Text,
    HorizontalAlignment,
    Position,
    Context,
)

ASSETS_PATH = join(dirname(dirname(__file__)), 'assets')


class TestContext(Context):
    image: Path
    title: str
    text: str


class FacebookPattern(Pattern):
    canvas: Canvas = Canvas(
        size=(1200, 630),
    )
    layers: List[Layer] = [
        Layer(
            Rectangle(
                background_color=(99, 99, 99),
                size=(1200, 630),
                point=Point(
                    x=0,
                    y=0,
                ),
            ),
        ),
        Layer(
            Rectangle(
                background_image=TestContext.var('image'),
                size=(458, 630),
                point=Point(
                    x=742,
                    y=0,
                ),
            ),
        ),
        Layer(
            Text(
                text=TestContext.var('title'),
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
                text=TestContext.var('text'),
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
        )
    ]


def test_version():
    assert __version__ == '0.0.1a'


def test_facebook():
    image = FacebookPattern(
        context=TestContext(
            title='WHAT THIS TIME? WHAT THIS TIME? WHAT THIS TIME?',
            text='This is adventure time!!! This is adventure time!!! This is adventure time!!! This is adventure time!!! This is adventure time!!! This is adventure time!!! This is adventure time!!!',
            image=join(ASSETS_PATH, 'Finn.jpg'),
        ),
    ).render()
    image.save(join(ASSETS_PATH, 'test.jpg'), format='JPEG')