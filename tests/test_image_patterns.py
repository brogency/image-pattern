from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Dict,
)
from os.path import join
from image_pattern import (
    __version__,
    HorizontalAlignment,
    VerticalAlignment,
)
from pytest import (
    raises,
    fixture,
)
from PIL import Image
from functools import reduce
from operator import add
from math import sqrt

from .patterns import (
    SimpleTestPattern,
    SmallTestPattern,
    SmallTestPatternContext,
    ComplexPattern,
    ComplexContext,
    OffsetPattern,
)
from .settings import ASSETS_PATH

if TYPE_CHECKING:
    from image_pattern import Pattern

SIMPLE_IMAGE_PATTERN = join(ASSETS_PATH, 'simple-pattern.jpg')
OFFSET_IMAGE_PATTERN = join(ASSETS_PATH, 'offset-pattern.jpg')


def test_version():
    assert __version__ == '0.0.16'


@fixture()
def simple_test_pattern():
    pattern = SimpleTestPattern()
    return pattern


@fixture()
def small_test_patterns():
    return {
        'small-align-left-top-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-center-top-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-right-top-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-left-center-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-center-center-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-right-center-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-left-bottom-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-center-bottom-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-right-bottom-jake.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='JAKE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-left-top-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-center-top-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-right-top-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-left-center-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-center-center-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-right-center-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-left-bottom-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-center-bottom-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-right-bottom-bmo.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='BMO',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-left-top-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-center-top-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-right-top-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.TOP,
            ),
        ),
        'small-align-left-center-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-center-center-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-right-center-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        ),
        'small-align-left-bottom-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-center-bottom-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.CENTER,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
        'small-align-right-bottom-ice.jpg': SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.RIGHT,
                vertical_alignment=VerticalAlignment.BOTTOM,
            ),
        ),
    }


@fixture()
def patterns():
    return {
        'fin-right-warning.jpg': ComplexPattern(
            context=ComplexContext(
                left_image=join(ASSETS_PATH, 'Finn-the-human.jpg'),
                right_image=join(ASSETS_PATH, 'Jake-the-dog.jpg'),
                title='FINN THE HUMAN',
                text='Finn the human. Finn the human. Finn the human. Finn the human. Finn the human. Finn the human.',
                layer_exists=True,
            )
        ),
        'fin-right.jpg': ComplexPattern(
            context=ComplexContext(
                left_image=join(ASSETS_PATH, 'Finn-the-human.jpg'),
                right_image=join(ASSETS_PATH, 'Jake-the-dog.jpg'),
                title='FINN THE HUMAN. FINN THE HUMAN.',
                text='Finn the human. Finn the human. Finn the human. Finn the human. Finn the human. Finn the human.',
                layer_exists=False,
            )
        ),
        'fin-right-empty-text.jpg': ComplexPattern(
            context=ComplexContext(
                left_image=join(ASSETS_PATH, 'Finn-the-human.jpg'),
                right_image=join(ASSETS_PATH, 'Jake-the-dog.jpg'),
                title='FINN THE HUMAN',
                layer_exists=False,
            )
        ),
    }


def test_simple_pattern(simple_test_pattern: Pattern):
    image = simple_test_pattern.render_to_blob()
    rms = _compare_result_and_purpose_images(image, SIMPLE_IMAGE_PATTERN)
    assert rms == 0


def test_small_test_patterns(small_test_patterns: Dict[str, Pattern]):
    for filename, pattern in small_test_patterns.items():
        image = pattern.render_to_blob()
        rms = _compare_result_and_purpose_images(image, join(ASSETS_PATH, filename))
        assert rms == 0


def test_vertical_alignment_errors():
    with raises(ValueError):
        assert SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment=HorizontalAlignment.LEFT,
                vertical_alignment='FROM SKY',
            ),
        )


def test_horizontal_alignment_errors():
    with raises(ValueError):
        assert SmallTestPattern(
            context=SmallTestPatternContext(
                text='ICE',
                background_color=(3, 202, 252),
                horizontal_alignment='TO LEFT',
                vertical_alignment=VerticalAlignment.CENTER,
            ),
        )


def test_image_patterns(patterns: Dict[str, Pattern]):
    for filename, pattern in patterns.items():
        rms = _compare_result_and_purpose_images(pattern.render_to_blob(), join(ASSETS_PATH, filename))
        assert rms == 0


def test_offset_pattern():
    pattern = OffsetPattern()
    image = pattern.render_to_blob()
    _compare_result_and_purpose_images(image, OFFSET_IMAGE_PATTERN)


def _compare_result_and_purpose_images(result_blob, purpose_file: str):
    result_image = Image.open(result_blob)
    purpose_image = Image.open(purpose_file)
    rms = _compare_images(
        result_image,
        purpose_image,
    )

    return rms


def _compare_images(source, purpose):
    source_histogram = source.histogram()
    purpose_histogram = purpose.histogram()
    rms = sqrt(
        reduce(
            add,
            map(
                lambda a, b: (a - b) ** 2,
                source_histogram,
                purpose_histogram,
            )
        ),
    )

    return rms
