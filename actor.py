import pygame
import colors

class Actor(pygame.sprite.DirtySprite):
    def __init__(self, pos, size, color = colors.WHITE, layer = 1):
        self.m_hasImage = False
        self.m_size = size
        self.m_position = pos
        self.m_color = color

        pygame.sprite.DirtySprite.__init__(self)
        self._updateImage()
        #self.image = pygame.Surface([50, 50])
        #self.image.fill(colors.RED_BROWN)
        #self.rect = self.image.get_rect()
        #self.rect.center = pos

        #self.dirty = 1
        self.visible = 1
        self._layer = layer

    def _updateImage(self):
        if self.m_hasImage:
            pass
            #TODO
        else:
            self.image = pygame.Surface(self.m_size)
            self.image.fill(self.m_color)
            self.rect = self.image.get_rect()
            self.rect.center = self.m_position
        self.dirty = 1

    def setPosition(self, x, y):
        self.m_position = x, y
        self.rect.center = x, y
        self.dirty = 1

    def resize(self, w, h):
        self.m_size = w, h
        if self.image:
            self.image = pygame.transform.scale(self.image, (w, h))
            self.rect.w = w
            self.rect.h = h
        self.dirty = 1