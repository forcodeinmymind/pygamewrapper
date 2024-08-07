"""
Ideas
-----
- class Pygame(pygame.sprite.Group)?
"""

import pygame
import pygame.freetype
import sys


class Pygame:
    """
    Most basic pygame setup; One-by-one from python docs

    _sprite = Sprite(<main_group>)

    Attributes
    ----------
    dt : float
        Delta time since previous call, sec
    """
    def __init__(self, size=(1366, 768)):
        if not pygame.get_init():
            pygame.init()
        pygame.display.set_caption(__name__)
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 30
        self.dt = 0
        self.size = size
        self.all_sprites = pygame.sprite.Group()
        self.eventqueue: list = []
        self.fgcolor = pygame.Color("tan1")
        self.bgcolor = pygame.Color("darkslategrey")

    def __str__(self):
        return "<Pygame>"

    def main(self):
        while self.running:
            self.eventqueue = pygame.event.get()
            if pygame.QUIT in [event.type for event in self.eventqueue]:
                self.running = False
            else:
                self.running = True
            self.running = self.eventhandle(self.running)
            self.update()
            self.render()
            self.tick()
        self.end()

    def eventhandle(self, running: bool) -> bool:
        return running

    def update(self) -> None:
        self.all_sprites.update()

    def tick(self) -> float:
        self.dt = self.clock.tick(self.fps) / 1000
        return self.dt

    def render(self) -> None:
        self.screen.fill(self.bgcolor)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def end(self):
        pygame.freetype.quit()
        pygame.quit()
        sys.exit()

    def get_size(self):
        return self.size

    def get_surface(self) -> pygame.Surface:
        return self.screen

    def get_dt(self) -> float:
        return self.dt

    def add_sprite(self, sprite: pygame.sprite.Sprite) -> int:
        if isinstance(sprite, pygame.sprite.Sprite):
            self.all_sprites.add(sprite)
            return len(self.all_sprites) - 1
        else:
            raise TypeError(f"{self}.addsprites({sprite=}) expected {pygame.sprite.Sprite}")

    def get_sprites(self):
        for sprite in self.all_sprites:
            yield sprite

    def get_events(self):
        return self.eventqueue


if __name__ == "__main__":
    app = Pygame()
    app.main()
