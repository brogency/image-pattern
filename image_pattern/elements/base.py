from __future__ import annotations
from typing import (
    Optional,
    Union,
    Tuple,
    TypeVar,
    Generic,
    TYPE_CHECKING,
)
from enum import Enum
from pydantic import BaseModel

from ..context import ContextVar

if TYPE_CHECKING:
    from PIL.Image import Image as PillowImage


class Point(BaseModel):
    x: int = 0
    y: int = 0

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


class Position(BaseModel):
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0


class HorizontalAlignment(str, Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class VerticalAlignment(str, Enum):
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'


class ImageMode(str, Enum):
    RGB = 'RGB'
    RGBA = 'RGBA'


class Drawer(BaseModel):
    size: Tuple[int, int]
    point: Point
    start_point: Point

    def draw(self, image: PillowImage) -> PillowImage:
        return image


T = TypeVar('T')


class Element(Generic[T], BaseModel):
    def collect_data(self, context: T):
        return {
            field: value.get_from_context(context) if isinstance(value, ContextVar) else value
            for field, value in self._iter()
        }

    def create_drawer(self, canvas: PillowImage, context: Optional[T] = None):
        data = self.collect_data(context)

        return Drawer(
            point=data['point'],
            size=(0, 0),
        )


class Positioned(Element):
    point: Point
    horizontal_alignment: Union[HorizontalAlignment, ContextVar] = HorizontalAlignment.LEFT.value
    vertical_alignment: Union[VerticalAlignment, ContextVar] = VerticalAlignment.TOP.value

    def _get_start_point(self, size):
        width, height = size
        return Point(
            x=self._get_start_x(width),
            y=self._get_start_y(height)
        )

    def _get_start_x(self, width: int):
        if self.horizontal_alignment == HorizontalAlignment.LEFT.value:
            x = self.point.x
        elif self.horizontal_alignment == HorizontalAlignment.RIGHT.value:
            x = self.point.x - width
        else:
            raise ValueError('Horizontal alignment must be LEFT or RIGHT')

        return x

    def _get_start_y(self, height: int) -> int:
        if self.vertical_alignment == VerticalAlignment.TOP.value:
            y = self.point.y
        elif self.vertical_alignment == VerticalAlignment.BOTTOM.value:
            y = self.point.y - height
        else:
            raise ValueError('Vertical alignment must be TOP or BOTTOM')

        return y
