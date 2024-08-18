"""pygamewrapper.pygamegui.text.main
Text Widget
1.0.0
2024-08-07
- shows a defined area in a multi-line text
  perhaps in different color
- has a vertical scrollbar
  perhaps also a horizontal scrollbar
- text input
"""

import sys
import os
import pygame
from pygamewrapper.sprite import Sprite
import pygamewrapper.pygamegui as pygamegui
import pygamewrapper.pgftwrapper as pgftwrapper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "strtool")))
import strtool


class Text(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.text: str = str()
        self.size_chr: tuple[int, int] = (32, 4)
        self.section_pos: int = 0
        self.cursor_pos: tuple[int, int] = (0, 0)
        self.render()

    def set_size_chr(self, size_chr: tuple[int, int]):
        self.size_chr = size_chr

    def update(self, *args, **kwargs) -> None:
        for event in kwargs["eventqueue"]:
            if event.type == pygame.TEXTINPUT:
                self.text += event.text
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
        self.render()

    def render(self) -> None:
        self.image = pygame.Surface(pygamegui.get_font().get_text_size_chr(self.size_chr))
        self.image.fill(self.bgcolor)
        conv_text = strtool.shape.newline_at(self.text, self.size_chr[0])
        pygamegui.get_font().render_text_basic(self.image, (0, 0), conv_text)
        pygame.draw.rect(self.image, self.fgcolor, self.image.get_rect(), 1)
        pygamegui.get_font().render_cursor(self.image, (0, 0), 