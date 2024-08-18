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
    """
    # font.set_font(name="Roboto Mono Regular", size=18)
    font.set_font(name="robotomono", size=18)
    """
    font_name = "roboto"
    for sys_font_name in pygame.freetype.get_fonts():
        if font_name in sys_font_name.lower():
            font_name = sys_font_name
            font.set_font(font_name, size=18)
            break
    else:
        raise KeyError(f"{font_name=} not in pygame.freetype.get_fonts()")
    if font.font.name == "FreeSans":
        raise KeyError(f"Requested {font_name=}. Currently used {font.font.name=}.")
    print(f"pygamegui.font={font}")
    print(font.str_attrs())

def get_font() -> FTWrapper:
    global font
    return font

def set_font(name: str, size: int):
    global font
    font = FTWrapper()
    font.set_font(name=name, size=size)