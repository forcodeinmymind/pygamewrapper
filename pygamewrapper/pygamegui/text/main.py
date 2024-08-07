import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', "pygamewrapper")))
from pygamewrapper.sprite import Sprite


class TextSprite(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.string: str = ""
        self.size_chr: tuple[int, int] = (8, 16)

    def set_size_chr(self, size_chr: tuple[int, int]):
        self.size_chr = size_chr

    def update(self, *args, **qwargs) -> None:
        pass
