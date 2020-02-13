from __future__ import annotations
from typing import (
    Optional,
    List,
    Tuple,
    Union,
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
    Positioned,
)
from ..context import (
    ContextVar,
)

if TYPE_CHECKING:
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
            x = self._get_x(font_width)
            y = self._get_y(line_index, self.line_height)
            draw.text((x, y), line, font=font, fill=self.font_color)

        return image

    def _get_x(self, text_width: int) -> int:
        if self.horizontal_alignment == HorizontalAlignment.LEFT.value:
            x = self.point.x
        elif self.horizontal_alignment == HorizontalAlignment.RIGHT.value:
            x = self.point.x - text_width
        else:
            raise ValueError('Horizontal alignment must be LEFT or RIGHT')

        return x

    def _get_y(self, line_index: int, text_height: int) -> int:
        start_y = self._get_first_line_y(self.line_height)
        diff = text_height * line_index

        if self.vertical_alignment == VerticalAlignment.TOP.value:
            y = start_y + diff
        elif self.vertical_alignment == VerticalAlignment.BOTTOM.value:
            y = start_y - diff
        else:
            raise ValueError('Vertical alignment must be TOP or BOTTOM')

        return y

    def _get_multiline_text(self, font: PillowImageFont, width: int) -> List[str]:
        line_length = int((width / (font.getsize(self.text)[0] / len(self.text))))
        text_lines = wrap(self.text, line_length)

        return text_lines

    def _get_first_line_y(self, text_height: int):
        if self.vertical_alignment == VerticalAlignment.TOP.value:
            y = self.point.y
        elif self.vertical_alignment == VerticalAlignment.BOTTOM.value:
            y = self.point.y - text_height
        else:
            raise ValueError('Vertical alignment must be TOP or BOTTOM')

        return y

    class Config:
        arbitrary_types_allowed = True


class Text(Positioned):
    _type: str = 'Text'
    font: Union[Path, ContextVar]
    font_size: Union[int, ContextVar] = 12
    font_color: Union[Tuple[int, int, int], ContextVar] = (0, 0, 0)
    text: Union[str, ContextVar]
    line_height: Union[int, ContextVar, None]
    margin: Union[Position, ContextVar] = Position()

    def create_drawer(self, canvas: PillowImage, context=None):
        data = self.collect_data(context)

        if data['text']:
            bounded_width, bounded_height = self._get_bounded_size(canvas)
            font = ImageFont.truetype(str(self.font.absolute()), size=self.font_size, encoding='UTF-8')
            text = self._get_multiline_text(data['text'], font, bounded_width)
            line_height = data['line_height'] or data['font_size'] + 4
            size = font.getsize_multiline('\n'.join(text), spacing=line_height - data['font_size'])
            start_point = self._get_start_point(size)

            return TextDrawer(
                point=data['point'],
                font=font,
                font_color=data['font_color'],
                text=text,
                line_height=line_height,
                horizontal_alignment=data['horizontal_alignment'],
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

    @staticmethod
    def _get_multiline_text(text, font: PillowImageFont, width: int) -> List[str]:
        font_width, _ = font.getsize(text)
        line_length = int((width / (font_width / len(text))))
        text_lines = wrap(text, line_length)

        return text_lines

    def _get_bounded_size(self, canvas: PillowImage) -> Tuple[int, int]:
        width, height = canvas.size

        bounded_width = self._get_bounded_width(width)
        bounded_height = self._get_bounded_height(height)

        return bounded_width, bounded_height

    def _get_bounded_width(self, width: int) -> int:
        if self.horizontal_alignment == HorizontalAlignment.LEFT.value:
            bounded_width = width - self.point.x - self.margin.right
        elif self.horizontal_alignment == HorizontalAlignment.RIGHT.value:
            bounded_width = self.point.x - self.margin.left
        else:
            raise ValueError('Horizontal alignment must be LEFT or RIGHT')

        return bounded_width

    def _get_bounded_height(self, height: int) -> int:
        if self.vertical_alignment == VerticalAlignment.TOP:
            bounded_height = height - self.point.y - self.margin.bottom
        elif self.vertical_alignment == VerticalAlignment.BOTTOM:
            bounded_height = self.point.y - self.margin.top
        else:
            raise ValueError('Vertical alignment must be TOP or BOTTOM')

        return bounded_height
