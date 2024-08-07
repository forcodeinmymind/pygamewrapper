"""Scrollbar
2024-08-01
1.0.0

- Track
- Thumb / Scroll box
- Buttons
"""


import pygame

# Scrollbar, vertical
def get_thumb(len_abs: int | float, \
              len_area: int | float, \
              pos_area: int | float, \
              track_rect: pygame.Rect) \
              -> pygame.Rect:
    scale = track_rect.h / len_abs if len_abs != 0 else 1.0
    x = track_rect.x
    y = track_rect.y + int((pos_area * scale) + 0.5)
    w = track_rect.w
    h = min(int((len_area * scale) + 0.5), track_rect.h - int((pos_area * scale) + 0.5))
    return pygame.Rect(x, y, w, h)

def draw_scrollbar(dest: pygame.Surface, \
                   fgcolor: pygame.Color, \
                   bgcolor: pygame.Color, \
                   scrollbar_rect: pygame.Rect, \
                   track_rect: pygame.Rect, \
                   len_abs: int | float, \
                   len_area: int | float, \
                   pos_area: int | float) -> None:
    pygame.draw.rect(dest, bgcolor, scrollbar_rect)
    pygame.draw.rect(dest, fgcolor, scrollbar_rect, 1)
    thumb = get_thumb(len_abs, len_area, pos_area, track_rect)
    thumb.x = scrollbar_rect.x + thumb.x
    thumb.y = scrollbar_rect.y + thumb.y
    pygame.draw.rect(dest, fgcolor, thumb)
