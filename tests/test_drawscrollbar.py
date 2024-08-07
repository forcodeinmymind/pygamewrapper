import sys
import os
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygamewrapper
pygamewrapper.draw.drawtext.keeplinebreaks = False
pygamewrapper.draw.drawtext.font_default = pygamewrapper.draw.drawtext.pygame.freetype.SysFont("PetMe64", 20)


class ScrollbarError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Application(pygamewrapper.Pygame):
    def __init__(self):
        super().__init__()
        self.data = "item0\nitem1\nitem2\n"
        self.text_pos = 0
        self.text_len = 5
    
    def eventhandle(self, running: bool) -> bool:
        for event in self.eventqueue:
            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_DOWN, pygame.K_PAGEDOWN) and \
                   len(self.data.splitlines()) <= self.text_len:
                    try:
                        raise ScrollbarError(
                            f"ScrollbarError: Move down [K_{pygame.key.name(event.key).upper().replace(" ", "")}] only possible if {len(self.data.splitlines())=} > {self.text_len=}")
                    except ScrollbarError as e:
                        print(e)
                if event.key in (pygame.K_UP, pygame.K_PAGEUP) and \
                   self.text_pos < 1:
                    try:
                        raise ScrollbarError(
                            f"ScrollbarError: Move up [K_{pygame.key.name(event.key).upper().replace(" ", "")}] only possible if {self.text_pos=} > 0")
                    except ScrollbarError as e:
                        print(e)

                if event.key == pygame.K_RETURN:
                    self.data += f"item{len(self.data.splitlines())}\n"
                elif event.key == pygame.K_DELETE:
                    self.data = str() if len(self.data.splitlines()) == 1 \
                                      else "\n".join(self.data.splitlines()[:-1]) + "\n"
                elif event.key == pygame.K_DOWN:
                    if len(self.data.splitlines()) > self.text_len:
                        self.text_pos = min(len(self.data.splitlines()) - self.text_len, \
                                            self.text_pos + 1)
                elif event.key == pygame.K_PAGEDOWN:
                    if len(self.data.splitlines()) > self.text_len:
                        self.text_pos = min(len(self.data.splitlines()) - self.text_len, \
                                            self.text_pos + self.text_len)
                elif event.key == pygame.K_END:
                    if len(self.data.splitlines()) > self.text_len:
                        self.text_pos = len(self.data.splitlines()) - self.text_len
                elif event.key == pygame.K_UP:
                    self.text_pos = max(0, self.text_pos - 1)
                elif event.key == pygame.K_PAGEUP:
                    self.text_pos = max(0, self.text_pos - self.text_len)
                elif event.key == pygame.K_HOME:
                    self.text_pos = 0
                else:
                    pass
        return running

    def render(self):
        self.screen.fill(self.bgcolor)
        self.all_sprites.draw(self.screen)

        # excerpt
        TEXT_POS = (64, 64)
        str_text_section = "".join(self.data.splitlines(True)[self.text_pos:self.text_pos + self.text_len])
        if len(self.data.splitlines()) < self.text_len:
            str_text_section += "\n" * (self.text_len - len(self.data.splitlines()))
        text_rect = pygamewrapper.draw.drawtext.draw_text(self.screen, TEXT_POS, str_text_section)
        pygamewrapper.draw.drawtext.draw_text(self.screen, \
                                              (TEXT_POS[0], TEXT_POS[1] + text_rect.h), \
                                              f"{os.linesep}{repr(self.data)=:}{os.linesep}{len(self.data.splitlines())=:}")
        pygamewrapper.draw.scrollbar(self.screen, \
                                     self.fgcolor, \
                                     self.bgcolor, \
                                     pygame.Rect(TEXT_POS[0] - 32, TEXT_POS[1], 32, text_rect.h), \
                                     pygame.Rect(2, 2, 32 - 4, text_rect.h - 4), \
                                     len(self.data.splitlines()), \
                                     self.text_len, \
                                     self.text_pos)
        pygame.display.flip()



if __name__ == "__main__":
    app = Application()
    pygamewrapper.draw.drawtext.font_default.fgcolor = app.fgcolor
    pygamewrapper.draw.drawtext.font_default.bgcolor = app.bgcolor

    app.main()
