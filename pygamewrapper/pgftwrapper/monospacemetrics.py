"""Check if a font is monospace
ChatGPT
1.0.0
2024-07-30
"""

import pygame.freetype


def is_monospace(font: pygame.freetype.Font, text: str) -> bool:
    char_widths = {char: font.get_rect(char).width for char in text}
    unique_widths = set(char_widths.values())
    return len(unique_widths) == 1
