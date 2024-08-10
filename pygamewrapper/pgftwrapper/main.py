import pygame
import pygame.freetype

from .constants import *
from .notdefmetrics import get_notdef_metrics
from .absmetrics import get_abs_metrics
from .monospacemetrics import is_monospace



class FTWrapperError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class FTWrapper:
    def __init__(self):
        self.file_calibration: str = "Codepage 850_manuel sorted.txt"

        self.font: pygame.freetype.Font | None = None
        # self.origin: bool = False
        # self.pad: bool = False
        self.monospace: bool = False

        self.abs_metrics_minx_min: int = 0
        self.abs_metrics_miny_min: int = 0
        self.abs_metrics_maxy_max: int = 0
        self.pen_x_zero: int = 0
        self.notdef_metrics: tuple[int, int, int, int, float, float] | None = None
        self.str_notdef: str = chr(1)
        self.linespace_factor: float = 1.0
        self.line_ascend: int = 0
        self.adv_mono: int | None = None

        self.keeplinebreaks: bool = True

        self.c_area = pygame.Color("gold")
        self.c_tile = pygame.Color("deepskyblue2")
        self.c_grapheme = pygame.Color("seagreen2")
        self.c_bb_text = pygame.Color("deepskyblue2")
        self.c_cursor_fgcolor = None
        self.c_cursor_bgcolor = None

        self.show_bb_area = True
        self.show_bb_tile = False
        self.show_bb_grapheme = False
        self.show_bb_text = False

    def __str__(self) -> str:
        return f"PygameFreeTypeWrapper({os.path.basename(self.font.path), self.font.size})"

    def str_attrs(self) -> str:
        string = str()
        for e in dir(self):
            if not callable(getattr(self, e)) and \
               e[0:2] != "__":
                string += f"{e}: {getattr(self, e)}\n"
        return string

    def set_font(self, name: str | None = None, size: int = 18) -> None:
        cur_font = self.font
        self.font = pygame.freetype.SysFont(name, size)
        if self.font.name == "FreeSans" and \
           name != "FreeSans":
            try:
                FTWrapperError(".set_font({name=}, {size=}) no corresponding font available")
            except FTWrapperError as error:
                print(error)
        if cur_font is not None:
            self.font.fgcolor = cur_font.fgcolor
            self.font.bgcolor = cur_font.bgcolor
            self.font.origin = cur_font.origin
            self.font.pad = cur_font.pad
        else:
            self.font.fgcolor = (255, 102, 102, 255)
            self.font.bgcolor = (  0,  51, 102, 255)
        self.c_cursor_fgcolor = self.font.fgcolor
        self.c_cursor_bgcolor = self.font.bgcolor
        self.set_notdef_metrics()
        self.set_abs_metrics()
        self.pen_x_zero = abs(self.abs_metrics_minx_min)
        self.set_linespace_factor(1.0)

    def set_notdef_metrics(self) -> None:
        cur_font_pad = self.font.pad
        self.font.pad = False
        r_notdef = self.font.get_rect(self.str_notdef)
        r_two_notdef = self.font.get_rect(self.str_notdef * 2)
        self.font.pad = cur_font_pad
        self.notdef_metrics = (r_notdef.x, \
                               r_notdef.x + r_notdef.w, \
                               r_notdef.y - r_notdef.h, \
                               r_notdef.y, \
                               float(r_two_notdef.w - r_notdef.w), \
                               float())

    def set_abs_metrics(self) -> None:
        """
        with open(self.file_calibration, "r", encoding='utf-8') as file:
            str_calibration = file.read()
        """
        minx_min = set()
        miny_min = set()
        maxy_max = set()

        for metrics in self.font.get_metrics(str_calibration):
            if metrics is not None:
                minx_min.add(metrics[MINX])
                miny_min.add(metrics[MINY])
                maxy_max.add(metrics[MAXY])

        minx_min.add(self.notdef_metrics[MINX])
        miny_min.add(self.notdef_metrics[MINY])
        maxy_max.add(self.notdef_metrics[MAXY])

        if not all((minx_min, miny_min, maxy_max)):
            NEWLINE = "NEWLINE"

            raise ValueError(f"{self}.get_abs_metrics({self.font.name}, {str_calibration:.10}...){NEWLINE}ERROR: Metrics partially or completely not available!")

        if min(minx_min) > 0:
            minx_min = {0, }

        self.abs_metrics_minx_min = min(minx_min)
        self.abs_metrics_miny_min = min(miny_min)
        self.abs_metrics_maxy_max = max(maxy_max)
        self.set_monospace(str_calibration)

    def set_monospace(self, str_calibration: str = ""):
        set_advx = set()
        for metrics in self.font.get_metrics(str_calibration):
            if metrics is not None:
                set_advx.add(metrics[ADVX])
            set_advx.add(self.notdef_metrics[ADVX])
        if len(set_advx) > 1:
            self.monospace = False
            self.adv_mono = None
        else:
            self.monospace = True
            self.adv_mono = set_advx.pop()

    def set_linespace_factor(self, factor: float = 1.0):
        self.linespace_factor = factor
        self.line_ascend = int((self.abs_metrics_maxy_max * self.linespace_factor) + 0.5)

    def set_line_ascend(self, px: int = 0):
        self.linespace_factor = px / self.abs_metrics_maxy_max
        self.line_ascend = px

    def conv_avdx(self, advx: float = 0.0):
        return int(advx)

    def get_area_topleft(self, area: pygame.Rect | None) -> tuple[int, int]:
        if area is None:
            return 0, 0
        else:
            return area.topleft

    # ...
    def convert_metrics(self, metrics = None) -> tuple[int, int, int, int, float, float]:
        if metrics is None:
            return self.notdef_metrics[MINX], self.notdef_metrics[MAXX], self.notdef_metrics[MINY], self.notdef_metrics[MAXY], self.conv_avdx(self.notdef_metrics[ADVX]), self.conv_avdx(self.notdef_metrics[ADVY])
        else:
            return metrics[MINX], metrics[MAXX], metrics[MINY], metrics[MAXY], self.conv_avdx(metrics[ADVX]), self.conv_avdx(metrics[ADVY])

    def get_metrics(self, text: str = ""):
        for metrics in self.font.get_metrics(text):
            yield self.convert_metrics(metrics)

    # string function
    def text_pos_to_index(self, string: str, pos: tuple[int, int]) -> int:
        return sum(len(str_line) for str_line in string.splitlines(self.keeplinebreaks)[0:pos[1]]) + pos[0]

    # local
    def get_linespace(self) -> int:
        return self.line_ascend - self.abs_metrics_miny_min

    def __get_pen_y(self, line: int = 0) -> int:
        return self.line_ascend + (line * self.get_linespace())

    def get_pen_x(self, str_line: str = "", column: int = 0) -> int:
        return self.pen_x_zero + sum(metrics[ADVX] for metrics in self.get_metrics(str_line[0:column]))

    def get_pen_right(self, str_line: str = "", column: int = 0) -> int:
        last_metrics = next(self.get_metrics(str_line[column])) if len(str_line) else [0, 0, 0, 0, 0.0, 0.0]
        return self.get_pen_x(str_line, column) + max(last_metrics[MAXX], last_metrics[ADVX])

    def get_text_width(self, text: str) -> int:
        if len(text):
            return max(self.get_pen_right(str_line, -1) for str_line in text.splitlines(self.keeplinebreaks))
        else:
            return self.pen_x_zero

    def get_text_size(self, text: str = "") -> tuple[int, int]:
        return self.get_text_width(text), \
               self.__get_pen_y(len(text.splitlines()) - 1) - self.abs_metrics_miny_min

    def get_text_size_max(self, size_chr: tuple[int, int]):
        pass

    # transform
    def tranform_to_global(self, axe: int = 0, dist: int = 0, area_axe: int = 0) -> int:
        return axe + dist - area_axe

    def transform_to_local(self, axe: int = 0, dist: int = 0, area_axe: int = 0) -> int:
        return axe - dist + area_axe

    def transform_rect_to_global(self, \
                                 dest: tuple[int, int] = (0, 0), \
                                 rect: pygame.Rect = None, \
                                 area: pygame.Rect = None, \
                                 do_clip: bool = True) \
                                 -> pygame.Rect:
        rect.x += dest[0]
        rect.y += dest[1]
        if area is not None:
            rect.x -= area.x
            rect.y -= area.y
            if do_clip:
                area = pygame.Rect(dest[0], dest[1], *area.size)
                rect = area.clip(rect)
        return rect


    # get rects

    def get_tile_rects(self, dest: tuple[int, int] = (0, 0), text: str = "", area: pygame.Rect = None):
        for line, str_line in enumerate(text.splitlines(self.keeplinebreaks)):
            pen_y = self.__get_pen_y(line)
            pen_x = self.pen_x_zero
            for column, metrics in enumerate(self.get_metrics(str_line)):
                rect_tile = pygame.Rect(pen_x, pen_y - self.line_ascend, \
                                        metrics[ADVX], self.get_linespace())
                rect_tile = self.transform_rect_to_global(dest, rect_tile, area)
                yield rect_tile
                pen_x += metrics[ADVX]

    def get_grapheme_rects(self, dest: tuple[int, int] = (0, 0), text: str = "", area: pygame.Rect = None) -> pygame.Rect:
        for line, str_line in enumerate(text.splitlines(self.keeplinebreaks)):
            pen_y = self.__get_pen_y(line)
            pen_x = self.pen_x_zero
            for metrics in self.get_metrics(str_line):
                rect_grapheme = pygame.Rect(pen_x + metrics[MINX], \
                                            pen_y - min(metrics[MAXY], self.line_ascend), \
                                            metrics[MAXX] - metrics[MINX], \
                                            min(metrics[MAXY], self.line_ascend) - metrics[MINY])

                rect_grapheme = self.transform_rect_to_global(dest, rect_grapheme, area)
                yield rect_grapheme
                pen_x += metrics[ADVX]

    def get_subtext_tile_rect(self, \
                              text: str = "", \
                              line: int = 0, \
                              start: int = 0, \
                              end: int = 0) -> pygame.Rect | None:
        if start < 0:
            raise IndexError()
        if start > end:
            raise IndexError()
        textline = text.splitlines(self.keeplinebreaks)[line]
        if start >= len(textline):
            return None
        if end >= len(textline):
            end = len(textline) - 1
        pen_x = self.pen_x_zero
        for column, metrics in enumerate(self.get_metrics(textline[0:end])):
            if column == start:
                pen_x_start = pen_x
            if column == end - 1:
                rect_right = pen_x + metrics[ADVX]
            pen_x += metrics[ADVX]
        return pygame.Rect(pen_x_start, \
                           self.__get_pen_y(line) - self.line_ascend, \
                           rect_right - pen_x_start, \
                           self.get_linespace())


    # collisions

    # TODO
    def collideline_y(self, \
                      length: int = 0, \
                      y: int = 0) \
                      -> int:
        line: int = y // self.get_linespace()
        if line < 0:
            return -1
        elif line >= length:
            return length
        else:
            return line

    def collideline_x(self, \
                      textline: str = "", \
                      x: int = 0) \
                      -> tuple[int, int]:

        # -> pen_x, column

        if x < 0:
            return self.pen_x_zero, -1
        column = 0
        column_x = self.pen_x_zero
        for grapheme in textline:
            metrics = next(self.get_metrics(grapheme))
            if column_x + max(metrics[ADVX], metrics[MAXX]) > x:
                break
            else:
                column += 1
                column_x += metrics[ADVX]
        return column_x, column

    def contains_x(self, \
                   textline: str = "", \
                   right: int = 0, \
                   start: int = 0, \
                   start_x: int | None = None) \
                   -> int:

        if start_x is None:
            column_x = self.get_pen_x(textline, start)
        column = start
        if right <= column_x:
            return start
        for grapheme in textline[start:]:
            metrics = next(self.get_metrics(grapheme))
            if column_x + min(0, metrics[MINX]) >= right:
                return column
            else:
                column += 1
                column_x += metrics[ADVX]
        return column

    def get_line_match(self, \
                       textline: str = "", \
                       line: int = 0, \
                       area: pygame.Rect | None = None, \
                       sectors: dict | None = None) \
                       -> tuple[int, int, int]:
        # -> pen_x, start, end
        # AREA_PEN_X = 0
        # AREA_START = 1
        # AREA_END = 2
        area_pen_x, area_start, area_end = self.get_line_match_area(textline, line, area)
        # ?! changed: collideline_x; if x < 0 -> -1, instead -> 0
        if area_start < 0:
            area_start = 0
        if sectors is None:
            return area_pen_x, area_start, area_end
        else:
            if line in sectors:
                if sectors[line][0] >= area_end:
                    start = area_end
                    start_x = self.get_pen_x(textline, start)
                    end = area_end
                elif sectors[line][1] < area_start:
                    start = area_start
                    start_x = self.get_pen_x(textline, start)
                    end = area_start
                else:
                    if sectors[line][0] <= area_start:
                        start = area_start
                        start_x = area_pen_x
                    else:
                        start = sectors[line][0]
                        start_x = self.get_pen_x(textline, start)
                    end = min(sectors[line][1], area_end)
            else:
                start = 0
                start_x = self.pen_x_zero
                end = 0
        return start_x, start, end

    def get_line_match_area(self, \
                            textline: str = "", \
                            line: int = 0, \
                            area: pygame.Rect | None = None) \
                            -> tuple[int, int, int]:

        if area is not None:
            if area.bottom <= self.__get_pen_y(line) - self.line_ascend or \
               area.top >= self.__get_pen_y(line) - self.abs_metrics_miny_min:
                start_area = self.pen_x_zero, 0
                end_area = 0
            else:
                start_area = self.collideline_x(textline, area.x)
                end_area = self.contains_x(textline, area.right)
        else:
            start_area = self.pen_x_zero, 0
            end_area = len(textline)
        return start_area[0], start_area[1], end_area

    def collidepoint_global(self, \
                            dest: tuple[int, int] = (0, 0), \
                            text: str = "",
                            pos: tuple[int, int] = (0, 0), \
                            area: pygame.Rect | None = None) \
                            -> tuple[int, int] | None:

        area_topleft = self.get_area_topleft(area)
        pos = self.transform_to_local(pos[X], dest[X], area_topleft[X]), \
              self.transform_to_local(pos[Y], dest[Y], area_topleft[Y])
        return self.collidepoint(text, pos, area)

    def collidepoint(self, \
                     text: str = "", \
                     pos: tuple[int, int] = (0, 0), \
                     area: pygame.Rect | None = None) \
                     -> tuple[int, int] | None:
        if area is not None:
            if not area.collidepoint(pos):
                return None
        line = self.collideline_y(len(text.splitlines(self.keeplinebreaks)), pos[Y])
        if 0 <= line < len(text.splitlines(self.keeplinebreaks)):
            return self.collideline_x(text.splitlines(self.keeplinebreaks)[line], pos[X])[1], line
        else:
            return 0, line

    # render
    def render_text_to(self, \
                       source: pygame.Surface = None, \
                       dest: tuple[int, int] = (0, 0), \
                       text: str = "", \
                       area: pygame.Rect | None = None, \
                       sectors: dict | None = None) \
                       -> str | None:

        str_diagnose = str()
        if area is None and \
            sectors is None and \
            self.linespace_factor >= 1.0:
            str_diagnose = str(self.render_text_basic(source, dest, text))
        else:
            str_diagnose = self.render_text_cut(source, dest, text, area, sectors)
        if self.show_bb_tile:
            self.render_tile_rects(source, dest, text, area)
        if self.show_bb_grapheme:
            self.render_grapheme_rects(source, dest, text, area)
        if self.show_bb_text:
            self.render_text_rect(source, dest, text, area)
        if self.show_bb_area:
            self.render_area_rect(source, dest, area)
        return str_diagnose

    def render_text_basic(self, \
                          source: pygame.Surface = None, \
                          dest: tuple[int, int] = (0, 0), \
                          text: str = "") \
                          -> pygame.Rect:
        for line, str_line in enumerate(text.splitlines(self.keeplinebreaks)):
            surf_line, rect_line = self.font.render(str_line)
            blit_x = dest[X] + self.pen_x_zero + rect_line.x
            blit_y = dest[Y] + self.__get_pen_y(line) - rect_line.y
            source.blit(surf_line, (blit_x, blit_y))
        # self.render_tile_rects(source, dest, text, None)

    def render_text_cut(self, \
                        source: pygame.Surface = None, \
                        dest: tuple[int, int] = (0, 0), \
                        text: str = "", \
                        area: pygame.Rect | None = None, \
                        sectors: dict | None = None) \
                        -> str | None:

        PEN_X = 0
        START = 1
        END = 2

        # str_diagnose = str()

        for line, textline in enumerate(text.splitlines(self.keeplinebreaks)):
            match = self.get_line_match(textline, line, area, sectors)
            if match[START] != match[END]:
                surf_line, rect_line = self.font.render(textline[match[START]:match[END]])

                # local_x = match[PEN_X] + rect_line.x
                # local_y = self.__get_pen_y(line) - rect_line.y

                ascend = min(rect_line.y, self.line_ascend, self.__get_pen_y(line) - area.y)
                blit_area_x = max(0, area.x - (match[PEN_X] + rect_line.x))

                blit_x = dest[X] - area.x + match[PEN_X] + rect_line.x + blit_area_x
                blit_y = dest[Y] - area.y + self.__get_pen_y(line) - ascend

                blit_area_w = area.right - (match[PEN_X] + rect_line.x + blit_area_x)

                blit_area_y = rect_line.y - ascend
                blit_area_h = min(self.__get_pen_y(line) - rect_line.y + rect_line.h, area.bottom) - (self.__get_pen_y(line) - ascend)

                source.blit(surf_line, (blit_x, blit_y), pygame.Rect(blit_area_x, blit_area_y, blit_area_w, blit_area_h))
                
                # str_diagnose += f"{line} {match}\n"
                
        return None


    # render rects
    def render_area_rect(self, \
                         source: pygame.Surface = None, \
                         dest: tuple[int, int] = (0, 0), \
                         area: pygame.Rect = None) \
                         -> None:

        if area is not None:
            pygame.draw.rect(source, self.c_area, pygame.Rect(dest, area.size), 1)

    def render_tile_rects(self, \
                          source: pygame.Surface = None, \
                          dest: tuple[int, int] = (0, 0), \
                          text: str = "", \
                          area: pygame.Rect = None):

        for rect_tile in self.get_tile_rects(dest, text, area):
            pygame.draw.rect(source, self.c_tile, rect_tile, 1)

    def render_grapheme_rects(self, \
                              source: pygame.Surface = None, \
                              dest: tuple[int, int] = (0, 0), \
                              text: str = "", \
                              area: pygame.Rect = None):
        for rect_grapheme in self.get_grapheme_rects(dest, text, area):
            rect_grapheme = None
            pygame.draw.rect(source, self.c_grapheme, rect_grapheme, 1)

    def render_text_rect(self, \
                         source: pygame.Surface = None, \
                         dest: tuple[int, int] = (0, 0), \
                         text: str = "", \
                         area: pygame.Rect = None):

        rect_text = pygame.Rect((0, 0), self.get_text_size(text))
        rect_text = self.transform_rect_to_global(dest, rect_text, area, True)
        pygame.draw.rect(source, self.c_bb_text, rect_text, 1)

    def render_sector_tile_rect(self, \
                                source: pygame.Surface = None, \
                                dest: tuple[int, int] = (0, 0), \
                                text: str = "", \
                                line: int = 0, \
                                start: int = 0, \
                                end: int = 0, \
                                area: pygame.Rect = None):

        rect_subtext = self.get_subtext_tile_rect(text, line, start, end)
        rect_subtext = self.transform_rect_to_global(dest, rect_subtext, area, True)
        pygame.draw.rect(source, self.c_tile, rect_subtext, 1)

    def render_cursor(self, \
                      source: pygame.Surface = None, \
                      dest: tuple[int, int] = (0, 0), \
                      text: str = "", \
                      line: int = 0, \
                      column: int = 0, \
                      area: pygame.Rect | None = None):
        self.render_cursor_type_line(source, dest, text, line, column, area)

    def render_cursor_type_line(self, \
                                source: pygame.Surface = None, \
                                dest: tuple[int, int] = (0, 0), \
                                text: str = "", \
                                line: int = 0, \
                                column: int = 0, \
                                area: pygame.Rect | None = None):

        CURSOR_WIDTH = 2

        rect_cursor = pygame.Rect(self.get_pen_x(text.splitlines(self.keeplinebreaks)[line], column), \
                                  self.__get_pen_y(line) - self.line_ascend, \
                                  CURSOR_WIDTH, \
                                  self.get_linespace())
        rect_cursor = self.transform_rect_to_global(dest, rect_cursor, area)
        pygame.draw.rect(source, self.c_cursor_fgcolor, rect_cursor)

    def __in_range(self, data, end: int) -> bool:
        """check if index/column is in range"""
        return -len(data) <= end < len(data)



