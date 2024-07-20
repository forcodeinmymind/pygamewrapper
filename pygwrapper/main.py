"""
Ideas
-----
- class Pygame(pygame.sprite.Group)?
"""

import pygame
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
        self.screen: pygame.Surface
        self.clock: pygame.time.Clock
        self.running = True
        self.fps = 30
        self.dt = 0
        self.size = size
        self.all_sprites = pygame.sprite.Group()

    def __str__(self):
        return "<Application>"

    def init(self, size: tuple[int, int] | None = None, fps: int | None = None):
        if size is not None:
            self.size = size
        if fps is not None:
            self.fps = fps
        pygame.display.set_caption(__name__)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.running = True

    def main(self):
        while self.running:
            self.running = self.eventhandle(self.running)
            self.update()
            self.all_sprites.update()
            self.render()
            self.tick()
        self.end()

    def eventhandle(self, running: bool) -> bool:
        self.eventqueue = list(pygame.event.get())
        for event in self.eventqueue:
            if event.type == pygame.QUIT:
                running = False
            else:
                pass
        return running

    def update(self) -> None:
        pass

    def tick(self):
        self.dt = self.clock.tick(self.fps) / 1000

    def render(self) -> None:
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def end(self):
        pygame.quit()
        pygame.freetype.quit()
        sys.exit()

    def get_size(self):
        return self.size

    def add_sprite(self, sprite: pygame.sprite.Sprite):
        if isinstance(sprite, pygame.sprite.Sprite):
            self.all_sprites.add(sprite)
        else:
            raise TypeError(f"{self}.addsprites({sprite=}) expected {pygame.sprite.Sprite}")

    def get_sprites(self):
        for sprite in self.all_sprites:
            yield sprite

    def get_events(self):
        return self.eventqueue


if __name__ == "__main__":
    app = Pygame()
    app.init()
    app.main()
