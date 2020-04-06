from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
)
from io import BytesIO
from pydantic import BaseModel

from .context import Context
from .elements import Canvas
from .layers import Layer

if TYPE_CHECKING:
    from PIL import Image


class Pattern(BaseModel):
    context: Optional[Context]
    canvas: Canvas
    layers: List[Layer] = []

    def render(self):
        image = self.canvas.get_image()

        for layer in self.layers:
            if layer.exist(context=self.context):
                image = layer.enhance_image(image, context=self.context)

        return image

    def render_to_blob(self, **save_kwargs):
        """
        :param save_kwargs: params for PIL.Image.save(), such as quality, optimize and progressive.
        :return: BytesIO object of image.
        """
        image = self.render()
        image_blob = get_image_blob(image, **save_kwargs)

        return image_blob


def get_image_blob(image: Image, **save_kwargs):
    blob = BytesIO()
    image.save(
        blob,
        'JPEG',
        **save_kwargs,
    )

    return blob
