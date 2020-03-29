from __future__ import annotations
from typing import (
    Tuple,
    Optional,
    TYPE_CHECKING,
)
from math import ceil

if TYPE_CHECKING:  # pragma: no cover
    from PIL import Image


def resize_image(
        image: Image,
        size: Tuple[int, int],
        center: Optional[Tuple[int, int]] = None,  # TODO: Do center position in Rectangle
):
    """
    Crop and resize the image depending on the center and size.
    !!! Warning. Image argument is not immutable.
    """
    # Proportional resizing
    image, center = scale_image(image, size, center=center)
    image = crop_image(image, size, center)
    # Purpose resizing
    image.resize(size)

    return image


def scale_image(
        image: Image,
        size: Tuple[int, int],
        center: Optional[Tuple[int, int]] = None,
):
    image_width, image_height = image.size
    width, height = size

    scaling_factor = max([width / image_width, height / image_height])
    scaling_width = ceil(image_width * scaling_factor)
    scaling_height = ceil(image_height * scaling_factor)

    center = center or (int(image_width / 2), int(image_height / 2))
    center_width, center_height = center
    center = (center_width * scaling_factor, center_height * scaling_factor)

    return image.resize((scaling_width, scaling_height)), center


def crop_image(
        image: Image,
        size: Tuple[int, int],
        center: Tuple[int, int],
):
    image_width, image_height = image.size
    width, height = size

    if image_width > width or image_height > height:
        half_width = int(width / 2)
        half_height = int(height / 2)
        center_x, center_y = center

        left = center_x - half_width
        right = center_x + half_width
        top = center_y - half_height
        bottom = center_y + half_height

        left, right = correct_size(
            left,
            right,
            0,
            image_width,
        )

        top, bottom = correct_size(
            top,
            bottom,
            0,
            image_height,
        )

        image = image.crop((left, top, right, bottom))

    return image


def correct_size(
        min_value: int,
        max_value: int,
        min_purpose_value: int,
        max_purpose_value: int,
):
    if min_value < min_purpose_value:
        correction = min_purpose_value - min_value
        min_value = min_purpose_value
        max_value = max_value + correction

        if max_value > max_purpose_value:
            max_value = max_purpose_value
    elif max_value > max_purpose_value:
        correction = max_purpose_value - max_value
        max_value = max_purpose_value
        min_value = min_value + correction

        if min_value < min_purpose_value:
            min_value = min_purpose_value

    return min_value, max_value
