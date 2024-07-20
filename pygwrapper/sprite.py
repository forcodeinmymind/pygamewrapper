__all__ = ("Sprite")

import pygame


class Sprite(pygame.sprite.Sprite):
    instance_ctr = 0
    game = None # <pygame.application>

    @staticmethod
    def add_instance(instance=None):
        Sprite.instance_ctr += 1
        return Sprite.instance_ctr -1

    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.id = Sprite.add_instance(self)
        self.fgcolor = (255, 0, 0)
        self.bgcolor = (255, 0, 0)
        self.image = pygame.Surface((64, 64))
        self.image.fill(self.bgcolor)
        self.rect = self.image.get_rect()
        self.dirty = 1
        self.visible = 1
        self.blendmode = 0
        # self.layer = 0
        
    def __str__(self) -> str:
        return f"<BasicSprite, {self.id}>"

    def update(self, *args, **qwargs) -> None:
        pass

    # Sprite.add(*groups)

    # Sprite.remove(*groups)

    # Sprite.kill()

    # Sprite.alive()

    # Sprite.groups()
