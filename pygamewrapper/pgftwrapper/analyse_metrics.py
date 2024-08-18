"""Functions for analysis pygame.freetype.Font metrics
1.0.0
2024-08-18
"""

import pygame
import pygame.freetype

SHOW_INDICIES = False
# used in: `.str_metrics_values(...)`


def get_metrics_values(font: pygame.freetype.Font, text: str, metrics_type: int) -> dict[int, list[int]]:
    """-> dict[metrics_value], list[text index where value occurs]"""
    metrics_values = dict()
    for index, metrics in enumerate(font.get_metrics(text)):
        if metrics is not None:
            if metrics[metrics_type] in metrics_values:
                metrics_values[metrics[metrics_type]].append(index)
            else:
                metrics_values[metrics[metrics_type]] = [index]
        elif None in metrics_values:
            metrics_values[None].append(index)
        else:
            metrics_values[None] = [index]
    return metrics_values

def str_metrics_values(font: pygame.freetype.Font, text: str, metrics_type: int) -> str:
    """-> str, list of all font metrics `metrics_type` in `text`
    optional: list of indices/chrs with corresponding metrics value
    """
    column0_w = 5
    len_str_indices = len(str(len(text)))
    str_data = str()
    for key, item in get_metrics_values(font, text, metrics_type).items():
        str_data += f"{const.metrics_type_names[metrics_type]}={str(key):>{column0_w}} {len(item):{len_str_indices}} chrs {int(((100/len(text)) * len(item)) + 0.5):3}%\n"
        if SHOW_INDICIES:
            str_data += "chr_index, chr_repr\n"
            for e in item:
                str_data += f"{e:0{len_str_indices}}, {repr(text[e])}\n"
    return str_data

def str_metrics_table(font: pygame.freetype.Font, text: str) -> str:
    str_data = str()
    str_data += f".str_metrics_table({font.name=}, text=...)\n"
    str_data += f"index   repr  minx   maxx   miny   maxy   advx   advy\n"
    for index, metrics in enumerate(font.get_metrics(text)):
        if metrics is None:
            str_data += f"{index:5}   {repr(text[index]):6}\n"
        else:
            str_data += f"{index:5}   {repr(text[index]):6}{metrics[0]:4}   {metrics[1]:4}   {metrics[2]:4}   {metrics[3]:4}   {metrics[4]:4}   {metrics[5]:4}\n"
    return str_data
        
    
    

if __name__ == "__main__":
    import constants as const
    
    if not pygame.get_init():
        pygame.init()
        
    font = pygame.freetype.SysFont(None, 16)
    print(f"{font.name=}\n")

    text = const.str_calibration
    print(str_metrics_values(font, text, const.MINX), "\n")
    print(str_metrics_values(font, text, const.ADVX), "\n")
    print(str_metrics_table(font, text))
