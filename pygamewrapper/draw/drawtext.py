"""drawtext.py
Module for drawing multi-line text with pygame.freetype
Date: 2024-08-02
Version: 1.0.0

#Attributes
linespace_factor
font_default
keeplinebreaks

# Functions
.set_keeplinebreaks()
.set_font()
.get_font()
.draw_text()
.get_pen_y()
.get_rect()
"""


import pygame
import pygame.freetype

if not pygame.init():
    pygame.init()
if not pygame.freetype.get_init():
    pygame.freetype.init()


linespace_factor: float = 1.0
font_default = pygame.freetype.SysFont("Roboto Mono Regular", 64)
font_default.fgcolor = pygame.Color("red")
keeplinebreaks = False


def set_keeplinebreaks(state: bool) -> None:
    global keeplinebreaks
    keeplinebreaks = state

def get_font() -> pygame.freetype.Font:
    return font_default

def set_font(name: str, size: int, bold: bool = False, italic: bool = False) -> pygame.freetype.Font:
    global font_default
    font_default = pygame.freetype.SysFont(name, size, bold, italic)
    return font_default

def draw_text(surf: pygame.Surface, \
              dest: tuple[int, int], \
              text: str, \
              fgcolor: pygame.Color | None = None, \
              bgcolor: pygame.Color | None = None, \
              style: int = pygame.freetype.STYLE_DEFAULT, \
              rotation: int = 0, \
              size: int | float | None = None, \
              font: pygame.freetype.Font | None = None) \
              -> pygame.Rect:
    """pygame.freetype.render_to()
    """
    if font is None:
        font = font_default
    if fgcolor is None:
        fgcolor = font.fgcolor
    orig_font_size = font.size
    if size is not None:
        font.size = size
    else:
        size = font.size

    i_line: int | None = None
    max_len_line = 0
    for i_line, str_line in enumerate(text.splitlines(keeplinebreaks)):
        s_text, r_text = font.render(str_line, fgcolor, bgcolor, style, rotation)
        blit_x = dest[0] + r_text.x
        blit_y = dest[1] - r_text.y + get_pen_y(i_line, font.size, font)
        surf.blit(s_text, (blit_x, blit_y))
    font.size = orig_font_size
    if i_line is not None:
        return pygame.Rect(dest, \
                           (max_len_line, \
                           (i_line + 1) * (int(font.get_sized_ascender(size) * linespace_factor + 0.5) - font.get_sized_descender(size)))
                           )
    else:
        return pygame.Rect(dest, (0, 0))

def get_pen_y(line_index: int, \
              size: int | float | None = None, \
              font: pygame.freetype.Font | None = None) \
              -> int:
    if font is None:
        font = font_default
    if size is None:
        size = font.size
    return int(font.get_sized_ascender(size) * linespace_factor + 0.5) + \
           (line_index * (int(font.get_sized_ascender(size) * linespace_factor + 0.5) - font.get_sized_descender(size)))

def get_rect(dest: tuple[int, int], \
             text: str, \
             size: int | float | None = None, \
             font: pygame.freetype.Font | None = None) \
             -> pygame.Rect:
    if font is None:
        font = font_default
    orig_font_size = font.size
    if size is not None:
        font.size = size
    else:
        size = font.size

    i_line: int | None = None
    max_line_len = 0
    for i_line, str_line in enumerate(text.splitlines(keeplinebreaks)):
        line_len = font.get_rect(str_line).right
        if line_len > max_line_len:
            max_line_len =  line_len
    font.size = orig_font_size
    if i_line is not None:
        return pygame.Rect(dest, (max_line_len, get_pen_y(i_line, size, font) - font.get_sized_descender(size)))
    else:
        return pygame.Rect(dest, (0, 0))



if __name__ == "__main__":
    import sys
    pygame.init()
    pygame.display.set_caption(__name__)
    screen = pygame.display.set_mode((1366, 768))
    running = True
    test_text = "%s\nabced\nefghi\njklmn\n" % (font_default.name, )

    screen.fill(pygame.Color("black"))

    DEST = (64, 64)
    pygame.draw.rect(screen, pygame.Color("deepskyblue2"), get_rect(DEST, test_text), 1)
    draw_text(screen, DEST, test_text)

    DEST_2 = (64, 512)
    TEXT_SIZE = 16
    pygame.draw.rect(screen, pygame.Color("deepskyblue2"), get_rect(DEST_2, test_text, size=TEXT_SIZE), 1)
    draw_text(screen, DEST_2, test_text, size=TEXT_SIZE)

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    else:
        pygame.freetype.quit()
        pygame.quit()
        sys.exit()
