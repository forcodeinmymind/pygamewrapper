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

import pygame
from pygamewrapper.sprite import Sprite
import pygamewrapper.pygamegui as pygamegui
import pygamewrapper.pgftwrapper as pgftwrapper

class Text(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.text: str = "`PygameGUI Text Widget` example text"
        self.size_chr: tuple[int, int] = (8, 16)
        self.section_pos: int = 0
        self.section_len: int = 5
        self.render()

    def set_size_chr(self, size_chr: tuple[int, int]):
        self.size_chr = size_chr

    def update(self, *args, **qwargs) -> None:
        pass

    def render(self) -> tuple[pygame.Surface, pygame.Rect]:
        self.image = pygame.Surface(pygamegui.get_font().get_text_size(self.text))
        self.image.fill(self.bgcolor)