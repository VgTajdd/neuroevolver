import pygame
import colors

class Actor(pygame.sprite.DirtySprite):
    def __init__(self, pos, size, color = colors.WHITE, layer = 1):
        pygame.sprite.DirtySprite.__init__(self)
        self.m_hasImage = False
        self.m_size = size
        self.m_position = pos
        self.m_color = color
        self.m_alpha = 255
        self._updateImage()
        self.visible = 1
        self._layer = layer

    def _updateImage(self):
        if self.m_hasImage:
            pass
            #TODO
        else:
            #self.image = pygame.Surface(self.m_size)
            #self.image.fill(self.m_color)
            self.image = pygame.Surface(self.m_size, pygame.SRCALPHA) # per-pixel alpha
            #self.image.fill((self.m_color[0], self.m_color[1], self.m_color[2], 128))
            self.image.fill(self.m_color + (self.m_alpha,))
            self.rect = self.image.get_rect()
            self.rect.center = self.m_position

    def setPosition(self, x, y):
        self.m_position = x, y
        self.rect.center = x, y
        self.dirty = 1

    def resize(self, w, h):
        self.m_size = w, h
        '''if self.image: #use this with loaded images
            self.image = pygame.transform.scale(self.image, (w, h))
            self.rect.w = w
            self.rect.h = h'''
        self.repaint()

    def repaint(self):
        self._updateImage() # this only updates the surface.
        self.dirty = 1      # this only makes the screen get drawn the 
                            # current surface in the next update.