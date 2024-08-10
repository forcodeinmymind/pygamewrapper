"""pygamegui.main
1.0.0
2024-08-07
"""
from pygamewrapper.pgftwrapper import FTWrapper

font: FTWrapper | None = None


def init():
    import pygame
    import pygame.freetype
    if not pygame.get_init():
        pygame.init()
    if not pygame.freetype.get_init():
        pygame.freetype.init()
    global font
    font = FTWrapper()
    font.set_font(name="Roboto Mono Regular", size=18)
    print(f"pygamegui.font={font}")
    print(font.str_attrs())

def get_font() -> FTWrapper:
    global font
    return font

def set_font(name: str, size: int):
    global font
    font = FTWrapper()
    font.set_font(name=name, size=size)