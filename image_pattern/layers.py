from __future__ import annotations
from typing import (
    List,
    Tuple,
    Union,
    Optional,
    Callable,
    TYPE_CHECKING,
)
from pydantic import BaseModel

from .context import Context
from .elements import (
    Rectangle,
    Text,
    Point,
)

if TYPE_CHECKING:  # pragma: no cover
    from PIL.Image import Image


class Area(BaseModel):
    point: Point
    size: Tuple[int, int]

    def intersect(self, point: Point):
        width, height = self.size
        return self.point.x + width > point.x >= self.point.x and self.point.y + height > point.y >= self.point.y

    def get_offset(self, point: Point):
        width, height = self.size
        width_offset = 0
        height_offset = self.point.y + height - point.y

        return width_offset, height_offset


def default_exist(context=None):
    return True


class Layer(BaseModel):
    elements: List[
        Union[
            Rectangle,
            Text,
        ]
    ]
    exist: Callable

    def __init__(self, *args, exist=None):
        elements = args
        exist = exist or default_exist
        super().__init__(elements=elements, exist=exist)

    def enhance_image(self, image: Image, context: Optional[Context] = None) -> Image:
        drawers = sorted(
            [element.create_drawer(image, context=context) for element in self.elements],
            key=lambda drawer: drawer.start_point.x + drawer.start_point.y,
        )
        filled_areas: List[Area] = []

        for drawer in drawers:
            intersections = [area for area in filled_areas if area.intersect(drawer.start_point)]

            for area in intersections:
                width_offset, height_offset = area.get_offset(drawer.start_point)

                drawer.start_point.x += width_offset
                drawer.start_point.y += height_offset
                drawer.point.x += width_offset
                drawer.point.y += height_offset

            image = drawer.draw(image)
            filled_areas.append(
                Area(
                    point=drawer.start_point,
                    size=drawer.size,
                ),
            )

        return image
