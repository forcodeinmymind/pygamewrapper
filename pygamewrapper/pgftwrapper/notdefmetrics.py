"""module to get metrics from notdef characters
"""

import pygame
import pygame.freetype


def get_notdef_metrics(font: pygame.freetype.Font) \
    -> tuple[int, int, int, int, float, float]:

    str_notdef = chr(0)
    cur_font_pad = font.pad
    font.pad = False

    r_notdef = self.font.get_rect(str_notdef)
    r_two_notdef = font.get_rect(str_notdef * 2)

    font.pad = cur_font_pad

    return r_notdef.x, \
           r_notdef.x + r_notdef.w, \
           r_notdef.y - r_notdef.h, \
           r_notdef.y, \
           float(r_two_notdef.w - r_notdef.w), \
           float()
