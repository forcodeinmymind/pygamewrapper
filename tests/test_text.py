import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pygamegui import pygamewrapper
from pygamegui import text


class Application(pygamewrapper.Pygame):
    def __init__(self):
        super().__init__()


app = Application()
text.TextSprite(app.all_sprites)
app.main()