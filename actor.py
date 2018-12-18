import pygame

class Actor(pygame.sprite.DirtySprite):
    def __init__(self, pos, layer = 1):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface([50, 50])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()

        self.rect.midtop = pos
        self.dirty = 1
        self.visible = 1
        self._layer = layer

    def setPosition(self, pos):
        self.rect.lefttop = pos
        self.dirty = 1

    def setSize(self, w, h):
        self.rect.w = pos
        self.dirty = 1