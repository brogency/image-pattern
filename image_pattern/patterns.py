from __future__ import annotations
from typing import List, Optional
from io import BytesIO
from pydantic import BaseModel

from .context import Context
from .elements import Canvas
from .layers import Layer


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

    def render_to_blob(self):
        image = self.render()
        image_blob = get_image_blob(image)

        return image_blob


def get_image_blob(image):
    blob = BytesIO()
    image.save(blob, 'JPEG')

    return blob
