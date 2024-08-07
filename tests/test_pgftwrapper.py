import sys
import os
import pygame
import pygame.freetype

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "strtool")))
import strtool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygamewrapper.pgftwrapper as pgftwrapper

"""
with open("./pgftwrapper/Codepage 850_manuel sorted.txt", "r", encoding='utf-8') as file:
    str_codepage850_manual = file.read()
"""
str_codepage850_manual = pgftwrapper.str_calibration

FONT_FGCOLOR = pygame.Color("gold")
FONT_BGCOLOR = pygame.Color("grey25")


def run(surf: pygame.Surface, clock: pygame.time.Clock) -> None:

    fps: int = 30
    dt: int = 0
    frame_ctr: int = 0
    do_run: bool = True

    font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 18)
    font.fgcolor = pygame.Color("gold")

    DEST_NOAREA = (32, 32)
    DEST_AREA = (960, 32)
    DEST_ALL_IN_ON = (960, pygame.display.get_surface().get_size()[1] // 2)
    AREA = pygame.Rect((32, 128, 480, 240))

    cursor_pos = (1, 1)

    while do_run:
        str_diagnose = str()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                do_run = False
            AREA = move_area(event, AREA)

        # update
        str_diagnose += f"update, frame:{frame_ctr: 06}\n"

        # render
        surf.fill(pygame.Color("black"))
        ftwrapper.render_text_to(surf, \
                                 DEST_NOAREA, \
                                 str_codepage850_manual)

        """
        str_data = ftwrapper.render_text_to(surf, \
                                            DEST_AREA, \
                                            str_codepage850_manual, \
                                            AREA, \
                                            TEXT_SECTOR)
        """

        str_data = ftwrapper.render_text_to(surf, \
                                            DEST_AREA, \
                                            str_codepage850_manual, \
                                            AREA, \
                                            None)

        str_data = str()
        str_diagnose += str_data

        # indicies tile rect
        TEXT_SECTOR = {2: (4, 16)}
        ftwrapper.render_sector_tile_rect(surf, \
                                          DEST_AREA, \
                                          str_codepage850_manual, \
                                          2, \
                                          4, \
                                          16, \
                                          AREA)

        # render cursor
        ftwrapper.render_cursor(surf, DEST_AREA, str_codepage850_manual, cursor_pos[1], cursor_pos[0], AREA)


        # TODO
        # collidepoint
        collidepoint = ftwrapper.collidepoint_global(DEST_AREA, str_codepage850_manual, pygame.mouse.get_pos(), AREA)

        str_diagnose += f"collidepoint {collidepoint}\n"

        # render utility

        # area on non-area
        pygame.draw.rect(surf, \
                         ftwrapper.c_area, \
                         pygame.Rect(DEST_NOAREA[0] + AREA.x, \
                                     DEST_NOAREA[1] + AREA.y, \
                                     AREA.w, AREA.h), \
                         1)

        # TODO: pgdrawmouse(font, surf, pygame.mouse.get_pos())
        # TODO: pgdrawtext(surf, (32, 900), str_diagnose, font, False)
        pygame.display.update()
        frame_ctr += 1
        dt = clock.tick(fps)

    else:
        pygame.quit()
        pygame.freetype.quit()
        sys.exit()


def move_area(event: pygame.event.Event, area: pygame.Rect):

    STEP = 1

    if pygame.key.get_mods() == pygame.KMOD_LSHIFT:
        STEP = 10

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            area.x += STEP
        elif event.key == pygame.K_LEFT:
            if pygame.key.get_mods() == pygame.KMOD_LCTRL:
                area.w -= STEP
            else:
                area.x -= STEP
        elif event.key == pygame.K_UP:
            if pygame.key.get_mods() == pygame.KMOD_LCTRL:
                area.h -= STEP
            else:
                area.y -= STEP
        elif event.key == pygame.K_DOWN:
            area.y += STEP
        else:
            pass
    return area


def move_cursor(event: pygame.event.Event, text: str, cursor_pos: tuple[int, int], keeplinebreaks: bool):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            return strtool.increment_cursor_horizontal(text, cursor_pos, keeplinebreaks, True)
        elif event.key == pygame.K_LEFT:
            return strtool.increment_cursor_horizontal(text, cursor_pos, keeplinebreaks, False)
        elif event.key == pygame.K_UP:
            return strtool.increment_cursor_vertical(text, cursor_pos, keeplinebreaks, True)
        elif event.key == pygame.K_DOWN:
            return strtool.increment_cursor_vertical(text, cursor_pos, keeplinebreaks, False)
        else:
            return cursor_pos
    else:
        return cursor_pos

    
# ...

if __name__ == "__main__":

    pygame.init()
    pygame.freetype.init()

    pygame.key.set_repeat(250, 125)

    surf: pygame.Surface = pygame.display.set_mode((1920, 1080))
    clock: pygame.time.Clock = pygame.time.Clock()

    ftwrapper = pgftwrapper.FTWrapper()
    ftwrapper.set_font("Consolas", 36)
    
    run(surf, clock)
