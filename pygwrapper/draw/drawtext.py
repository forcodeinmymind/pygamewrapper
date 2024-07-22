import sys
import pygame
import pygame.freetype

if not pygame.freetype.get_init():
    pygame.freetype.init()


linespace_factor: float = 1.0
font_default = pygame.freetype.SysFont("Roboto Mono Regular", 20)
font_default.fgcolor = pygame.Color("red")
keeplinebreaks = True


def draw_text(surf: pygame.Surface, \
              dest: tuple[int, int], \
              text: str, \
              fgcolor: pygame.Color | None = None, \
              bgcolor: pygame.Color | None = None, \
              font: pygame.freetype.Font | None = None) -> pygame.Rect:
    """pygame.freetype.render_to()
    """
    if font is None:
        font = font_default
    if fgcolor is None:
        fgcolor = font.fgcolor
    if bgcolor is None:
        bgcolor = font.bgcolor
    for i_line, str_line in enumerate(text.splitlines(keeplinebreaks)):
        s_text, r_text = font.render(str_line, fgcolor, bgcolor)
        blit_x = dest[0] + r_text.x
        blit_y = dest[1] + int(font.get_sized_ascender() * linespace_factor) - r_text.y \
                 + (i_line * (int(font.get_sized_ascender() * linespace_factor) - font.get_sized_descender()))
        surf.blit(s_text, (blit_x, blit_y))

def end():
    pygame.freetype.quit()


if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption(__name__)
    screen = pygame.display.set_mode((1366, 768))
    running = True
    test_text = "abced\nefghi\njklmn"

    screen.fill(pygame.Color("black"))
    draw_text(screen, (64, 64), test_text)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    else:
        end()
        pygame.quit()
        sys.exit()
