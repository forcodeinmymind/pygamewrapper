import sys
import os
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygamewrapper
pygamewrapper.draw.drawtext.keeplinebreaks = False
pygamewrapper.draw.drawtext.font_default = pygamewrapper.draw.drawtext.pygame.freetype.SysFont("Zig", 20)


class Application(pygamewrapper.Pygame):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = Application()

    app.main()
