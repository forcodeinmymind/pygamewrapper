import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygamewrapper
import string


class Application(pygamewrapper.Pygame):
    def __init__(self, size=(1366, 768)):
        super().__init__(size)


str_test = string.printable
str_test = '\n'.join(str_test[i:i + 12] for i in range(0, len(str_test), 12))

app = Application((1024, 576))
pygamewrapper.pygamegui.init()
pygamewrapper.pygamegui.Text(app.all_sprites)
list(app.get_sprites())[-1].text = str_test
app.main()
