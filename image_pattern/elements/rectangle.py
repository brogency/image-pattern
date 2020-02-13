from __future__ import annotations
from typing import (
    Optional,
    Tuple,
    Union,
    TYPE_CHECKING,
)

from pathlib import Path
from PIL import (
    Image,
    ImageEnhance,
)

from .base import (
    Positioned,
    Drawer,
    ImageMode,
    HorizontalAlignment,
    VerticalAlignment,
)
from .canvas import Canvas
from ..size import resize_image
from ..context import ContextVar

if TYPE_CHECKING:
    from PIL.Image import Image as PillowImage


class RectangleDrawer(Drawer):
    brightness: int = 0
    background_image: Optional[Path]
    background_color: Tuple[int, int, int] = (255, 255, 255)
    _image_mode: ImageMode = ImageMode.RGBA

    def draw(self, image: PillowImage) -> PillowImage:
        overlay_image = self.get_image()
        image.paste(overlay_image, self.start_point.to_tuple())

        return image

    def get_image(self) -> PillowImage:
        if self.background_image:
            image = Image.open(self.background_image)
        else:
            image = Image.new(self._image_mode, self.size, self.background_color)

        image = image.convert(self._image_mode) if not image.mode == self._image_mode else image
        image = self._resize_image(image)

        return image

    def _enhance(self, image: PillowImage) -> PillowImage:
        if self.brightness:
            image = ImageEnhance.Brightness(image).enhance(self.brightness)

        return image

    def _resize_image(self, image: PillowImage) -> PillowImage:
        return resize_image(image, self.size)


class Rectangle(Positioned, Canvas):
    _type: str = 'Rectangle'
    brightness: Union[int, ContextVar] = 0
    background_image: Union[Path, ContextVar, None]
    background_color: Union[Tuple[int, int, int], ContextVar] = (255, 255, 255)

    def create_drawer(self, canvas: PillowImage, context=None):
        data = self.collect_data(context)
        start_point = self._get_start_point(self.size)

        return RectangleDrawer(
            point=data['point'],
            size=data['size'],
            brightness=data['brightness'],
            background_image=data['background_image'],
            background_color=data['background_color'],
            start_point=start_point,
        )