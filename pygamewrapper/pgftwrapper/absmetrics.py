"""pygame freetype wrapper module to get absolut character metrics of given font
"""

import pygame.freetype


def get_abs_metrics(font: pygame.freetype.Font, \
                    str_calibration: str, \
                    notdef_metrics: tuple[int, int, int, int, float, float] | None) \
    -> tuple[int, int, int, int, float, float]:
    """get absolute metrics of `str_calibration` with `font`
    """

    MINX, MAXX, MINY, MAXY, ADVX, ADVY = range(6)

    minx = set()
    maxx = set()
    miny = set()
    maxy = set()
    advx = set()
    advy = set()

    for metrics in font.get_metrics(str_calibration):
        if metrics is not None:
            minx.add(metrics[MINX])
            maxx.add(metrics[MAXX])
            miny.add(metrics[MINY])
            maxy.add(metrics[MAXY])
            advx.add(metrics[ADVX])
            advy.add(metrics[ADVY])

    if notdef_metrics is not None:
        minx.add(self.notdef_metrics[MINX])
        maxx.add(self.notdef_metrics[MAXX])
        miny.add(self.notdef_metrics[MINY])
        maxy.add(self.notdef_metrics[MAXY])
        advx.add(self.notdef_metrics[ADVX])
        advy.add(self.notdef_metrics[ADVY])

    if not all((minx, maxx, miny, maxy, advx, advy)):
        NEWLINE = "NEWLINE"
        raise ValueError(f"{self}.get_abs_metrics({self.font.name}, {str_calibration:.10}...){NEWLINE}ERROR: Metrics partially or completely not available!")

    if min(minx) > 0:
        minx = {0, }

    return min(minx), max(maxx), min(miny), max(maxy), max(advx), max(advy)


if __name__ == "__main__":
    import pygame
    import pygame.freetype
    pygame.init()
    pygame.freetype.init()
    
    str_calibration = r" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"
    font = pygame.freetype.SysFont(None, 16)
    abs_metrics = get_abs_metrics(font, str_calibration, None)
    print(abs_metrics)
    
