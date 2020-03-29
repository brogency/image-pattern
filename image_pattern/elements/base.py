from __future__ import annotations
from typing import (
    Optional,
    Union,
    Tuple,
    TypeVar,
    Generic,
    TYPE_CHECKING,
)
from abc import ABCMeta, abstractmethod
from enum import Enum
from pydantic import BaseModel, Extra
from six import add_metaclass

from ..context import ContextVar

if TYPE_CHECKING:  # pragma: no cover
    from PIL.Image import Image as PillowImage


class Point(BaseModel):
    x: int = 0
    y: int = 0

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y

    class Config:
        extra = Extra.forbid


class Position(BaseModel):
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0

    class Config:
        extra = Extra.forbid


class HorizontalAlignment(str, Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CENTER = 'CENTER'


class VerticalAlignment(str, Enum):
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    CENTER = 'CENTER'


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


@add_metaclass(ABCMeta)
class Element(Generic[T], BaseModel):
    point: Point
    horizontal_alignment: Union[HorizontalAlignment, ContextVar] = HorizontalAlignment.LEFT
    vertical_alignment: Union[VerticalAlignment, ContextVar] = VerticalAlignment.TOP

    def collect_data(self, context: T):
        return {
            field: value.get_from_context(context) if isinstance(value, ContextVar) else value
            for field, value in self._iter()
        }

    @abstractmethod
    def create_drawer(self, canvas: PillowImage, context: Optional[T] = None):
        raise NotImplementedError  # pragma: no cover

    def _get_start_point(
            self,
            horizontal_alignment: HorizontalAlignment,
            vertical_alignment: VerticalAlignment,
            size,
            **kwargs
    ):
        width, height = size
        x = self._get_start_x(horizontal_alignment, width, **kwargs)
        y = self._get_start_y(vertical_alignment, height, **kwargs)
        return Point(
            x=x,
            y=y,
        )

    def _get_start_x(self, horizontal_alignment: HorizontalAlignment, width: int, **kwargs):
        if horizontal_alignment == HorizontalAlignment.LEFT:
            x = self.point.x
        elif horizontal_alignment == HorizontalAlignment.RIGHT:
            x = self.point.x - width
        else:  # Center
            x = self.point.x - int(width / 2)

        return x

    def _get_start_y(self, vertical_alignment: VerticalAlignment, height: int, **kwargs) -> int:
        if vertical_alignment == VerticalAlignment.TOP:
            y = self.point.y
        elif vertical_alignment == VerticalAlignment.BOTTOM:
            y = self.point.y - height
        else:  # Center
            y = self.point.y - int(height / 2)

        return y

