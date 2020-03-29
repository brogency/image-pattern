from __future__ import annotations
from typing import (
    List,
    Tuple,
    Union,
    Optional,
    TYPE_CHECKING,
)
from pathlib import Path
from textwrap import wrap
from PIL import (
    ImageFont,
    ImageDraw,
)
from PIL.ImageFont import FreeTypeFont as PillowImageFont

from .base import (
    Drawer,
    Position,
    HorizontalAlignment,
    VerticalAlignment,
    Element,
)
from ..context import (
    ContextVar,
)

if TYPE_CHECKING:  # pragma: no cover
    from PIL.Image import Image as PillowImage


class TextDrawer(Drawer):
    font: PillowImageFont
    font_color: Tuple[int, int, int] = (0, 0, 0)
    text: List[str]
    line_height: int
    horizontal_alignment: HorizontalAlignment = HorizontalAlignment.LEFT.value
    vertical_alignment: VerticalAlignment = VerticalAlignment.TOP.value
    margin: Position = Position()

    def draw(self, image: PillowImage) -> PillowImage:
        return self.draw_text(image, self.text, self.font)

    def draw_text(self, image: PillowImage, text: List[str], font: PillowImageFont):
        draw = ImageDraw.Draw(image)

        for line_index, line in enumerate(text):
            font_width, _ = font.getsize(line)
            _, height_offset = font.getoffset(line)
            x = self._get_x(font_width)
            y = self._get_y(line_index, self.line_height, height_offset)
            draw.text((x, y), line, font=font, fill=self.font_color)

        return image

    def _get_x(self, text_width: int) -> int:
        if self.horizontal_alignment == HorizontalAlignment.LEFT:
            x = self.point.x + self.margin.left
        elif self.horizontal_alignment == HorizontalAlignment.RIGHT:
            x = self.point.x - text_width
        else:  # Center
            x = self.point.x - int(text_width / 2)

        return x

    def _get_y(self, line_index: int, text_height: int, offset: int = 0) -> int:
        start_y = self._get_first_line_y(offset=offset)
        diff = text_height * line_index
        return start_y + diff

    def _get_first_line_y(self, offset: int = 0):
        _, height = self.size

        if self.vertical_alignment == VerticalAlignment.TOP:
            y = self.point.y
        elif self.vertical_alignment == VerticalAlignment.BOTTOM:
            y = self.point.y - height
        else:  # Center
            y = self.point.y - int(height / 2) - int(offset / 2)

        return y + self.margin.top

    class Config:
        arbitrary_types_allowed = True


class Text(Element):
    _type: str = 'Text'
    font: Union[Path, ContextVar]
    font_size: Union[int, ContextVar] = 12
    font_color: Union[Tuple[int, int, int], ContextVar] = (0, 0, 0)
    text: Union[str, ContextVar]
    line_height: Union[int, ContextVar, None]
    margin: Union[Position, ContextVar, None]

    def __init__(self, **kwargs):
        kwargs['margin'] = kwargs.get('margin', Position())
        super().__init__(**kwargs)

    def create_drawer(self, canvas: PillowImage, context=None):
        data = self.collect_data(context)

        if data['text']:

            bounded_width, bounded_height = self._get_bounded_size(
                canvas,
                data['horizontal_alignment'],
                data['vertical_alignment'],
                margin=data['margin'],
            )
            font = ImageFont.truetype(str(self.font.absolute()), size=self.font_size, encoding='UTF-8')
            text = self._get_multiline_text(data['text'], font, bounded_width)
            line_height = data['line_height'] or font.getsize(data['text'])[1]
            size = font.getsize_multiline('\n'.join(text), spacing=line_height - data['font_size'])
            start_point = self._get_start_point(
                data['horizontal_alignment'],
                data['vertical_alignment'],
                size,
                margin=data.get('margin')
            )

            return TextDrawer(
                point=data['point'],
                font=font,
                font_color=data['font_color'],
                text=text,
                line_height=line_height,
                horizontal_alignment=data['horizontal_alignment'],
                vertical_alignment=data['vertical_alignment'],
                margin=data['margin'],
                size=size,
                start_point=start_point,
            )
        else:
            return Drawer(
                size=(0, 0),
                point=data['point'],
                start_point=data['point'],
            )

    def _get_start_y(
            self,
            vertical_alignment: VerticalAlignment,
            height: int,
            margin: Optional[Position] = None,
            **kwargs,
    ) -> int:
        start_y = super()._get_start_y(vertical_alignment, height, **kwargs)
        return start_y + margin.top if margin else start_y

    def _get_start_x(
            self,
            horizontal_alignment: HorizontalAlignment,
            width: int,
            margin: Optional[Position] = None,
            **kwargs,
    ) -> int:
        start_x = super()._get_start_x(horizontal_alignment, width, **kwargs)
        return start_x + margin.left if margin else start_x

    @staticmethod
    def _get_multiline_text(text, font: PillowImageFont, width: int) -> List[str]:
        font_width, _ = font.getsize(text)
        line_length = int((width / (font_width / len(text))))
        text_lines = wrap(text, line_length)

        return text_lines

    def _get_bounded_size(
            self,
            canvas: PillowImage,
            horizontal_alignment: HorizontalAlignment,
            vertical_alignment: VerticalAlignment,
            margin: Position = None,
    ) -> Tuple[int, int]:
        width, height = canvas.size

        bounded_width = self._get_bounded_width(horizontal_alignment, width, margin=margin)
        bounded_height = self._get_bounded_height(vertical_alignment, height)

        return bounded_width, bounded_height

    def _get_bounded_width(
            self,
            horizontal_alignment: HorizontalAlignment,
            width: int,
            margin: Position = None,
    ) -> int:
        margin = margin or Position()
        if horizontal_alignment == HorizontalAlignment.LEFT:
            bounded_width = width - self.point.x - margin.right
        elif horizontal_alignment == HorizontalAlignment.RIGHT:
            bounded_width = self.point.x - margin.left
        else:  # Center
            bounded_width = width - margin.left - margin.right

        return bounded_width

    def _get_bounded_height(
            self,
            vertical_alignment: VerticalAlignment,
            height: int,
            margin: Position = None,
    ) -> int:
        margin = margin or Position()
        if vertical_alignment == VerticalAlignment.TOP:
            bounded_height = height - self.point.y - margin.bottom
        elif vertical_alignment == VerticalAlignment.BOTTOM:
            bounded_height = self.point.y - margin.top
        else:  # Center
            bounded_height = height - margin.top - margin.bottom

        return bounded_height
