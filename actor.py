import pygame
import colors

class Actor(pygame.sprite.DirtySprite):
    def __init__(self, pos, layer = 1):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface([50, 50])
        self.image.fill(colors.RED_BROWN)
        self.rect = self.image.get_rect()

        self.rect.center = pos
        self.dirty = 1
        self.visible = 1
        self._layer = layer

    def setPosition(self, x, y):
        self.rect.center = x, y
        self.dirty = 1

    def resize(self, w, h):
        if self.image:
            self.image = pygame.transform.smoothscale(self.image, (w, h))
            self.rect.w = w
            self.rect.h = h
        self.dirty = 1