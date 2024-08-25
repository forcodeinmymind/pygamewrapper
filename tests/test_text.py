import os
import sys
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygamewrapper
import string

pygamewrapper.pygamegui.init()
pygamewrapper.pygamegui.get_font().font.fgcolor = pygamewrapper.main.pygame.Color("tan1")
pygamewrapper.pygamegui.get_font().font.bgcolor = pygamewrapper.main.pygame.Color("darkslategrey")
# pygamewrapper.pygamegui.get_font().keepends = True


class Application(pygamewrapper.Pygame):
    def __init__(self, size=(1366, 768)):
        super().__init__(size)
        self.text_input: str = str()

    def eventhandle(self, running: bool) -> bool:
        for event in self.eventqueue:
            if event.type == pygame.TEXTINPUT:
                self.text_input += event.text
        return running

    def update(self) -> None:
        for sprite in self.get_sprites():
            sprite.update(dt=self.dt, eventqueue=self.eventqueue)


str_test = string.printable
# str_test = '\n'.join(str_test[i:i + 12] for i in range(0, len(str_test), 12))

app = Application((1024, 576))

pygamewrapper.pygamegui.Text(app.all_sprites)
text_widget = list(app.get_sprites())[-1]
str_test = '\n'.join(str_test[i:i + text_widget.size_chr[0]] for i in range(0, len(str_test), text_widget.size_chr[0]))
text_widget.fgcolor = pygame.Color("tan1")
text_widget.bgcolor = pygame.Color("darkslategrey")
# text_widget.text = str_test
# text_widget.render()

app.main()
