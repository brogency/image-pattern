from __future__ import annotations
from typing import (
    Tuple,
    Union,
    TYPE_CHECKING,
)
from PIL import Image

from .base import (
    Drawer,
    Element,
    ImageMode,
)
from ..context import (
    ContextVar,
)

if TYPE_CHECKING:
    from PIL.Image import Image as PillowImage


class Canvas(Element):
    _type: str = 'Canvas'
    size: Union[Tuple[int, int], ContextVar]
    _image_mode: ImageMode = ImageMode.RGB

    def get_image(self) -> PillowImage:
        return Image.new(self._image_mode, self.size)

