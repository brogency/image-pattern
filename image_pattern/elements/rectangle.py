from __future__ import annotations
from typing import (
    Optional,
    Tuple,
    Union,
    TYPE_CHECKING,
)
from io import BytesIO
from pathlib import Path
from PIL import (
    Image,
    ImageEnhance,
)

from .base import (
    Element,
    Drawer,
    ImageMode,
)
from .canvas import Canvas
from ..size import resize_image
from ..context import ContextVar

if TYPE_CHECKING:  # pragma: no cover
    from PIL.Image import Image as PillowImage


class RectangleDrawer(Drawer):
    brightness: Optional[float]
    background_image: Union[BytesIO, Path, None]
    background_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]] = (255, 255, 255)
    alpha: Optional[int]
    _image_mode: ImageMode = ImageMode.RGBA

    class Config:
        arbitrary_types_allowed = True

    def draw(self, image: PillowImage) -> PillowImage:
        overlay_image = self.get_image()
        image.paste(overlay_image, self.start_point.to_tuple(), mask=overlay_image)

        return image

    def get_image(self) -> PillowImage:
        if self.background_image:
            image = Image.open(self.background_image)
        else:
            background_color = (
                *self.background_color,
                self.alpha,
            ) if self.background_color and self.alpha is not None and \
                 len(self.background_color) == 3 else self.background_color
            image = Image.new(self._image_mode, self.size, background_color)

        image = image.convert(self._image_mode) if not image.mode == self._image_mode else image
        image = self._resize_image(image)
        image = self._enhance(image)

        return image

    def _enhance(self, image: PillowImage) -> PillowImage:
        if self.brightness is not None:
            image = ImageEnhance.Brightness(image).enhance(self.brightness)

        if self.alpha is not None:
            image.putalpha(self.alpha)

        return image

    def _resize_image(self, image: PillowImage) -> PillowImage:
        return resize_image(image, self.size)


class Rectangle(Element, Canvas):
    _type: str = 'Rectangle'
    brightness: Union[float, ContextVar, None]
    background_image: Union[BytesIO, Path, ContextVar, None]
    background_color: Union[Tuple[int, int, int], Tuple[int, int, int, int], ContextVar] = (255, 255, 255)
    alpha: Union[int, ContextVar, None]

    class Config:
        arbitrary_types_allowed = True

    def create_drawer(self, canvas: PillowImage, context=None):
        data = self.collect_data(context)
        start_point = self._get_start_point(
            data['horizontal_alignment'],
            data['vertical_alignment'],
            self.size,
        )

        return RectangleDrawer(
            point=data['point'],
            size=data['size'],
            brightness=data['brightness'],
            background_image=data['background_image'],
            background_color=data['background_color'],
            start_point=start_point,
            alpha=data['alpha'],
        )
