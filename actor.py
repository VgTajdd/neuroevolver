import pygame
import colors

class Actor(pygame.sprite.DirtySprite):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        pygame.sprite.DirtySprite.__init__(self)
        self.m_imagePath = imagePath
        self.m_size = size
        self.m_position = pos
        self.m_color = color
        self.m_alpha = alpha
        self.m_supportAlpha = True
        self._updateImage()
        self.visible = 1
        self._layer = layer
        # Rotation vars.
        self._imageCache = None
        self.m_angle = 0

    def _updateImage(self):
        if self.m_imagePath:
            if self.m_supportAlpha:
                self.image = pygame.image.load(self.m_imagePath).convert_alpha()
            else:
                self.image = pygame.image.load(self.m_imagePath).convert()
            self.image = pygame.transform.smoothscale(self.image, self.m_size)
        else:
            if self.m_supportAlpha:
                self.image = pygame.Surface(self.m_size, pygame.SRCALPHA) # per-pixel alpha
                self.image.fill(self.m_color + (self.m_alpha,))
            else:
                self.image = pygame.Surface(self.m_size)
                self.image.fill(self.m_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.m_position

    def setImage(self, imagePath):
        self.m_imagePath = imagePath
        self.repaint()

    def setPosition(self, x, y):
        self.m_position = x, y
        self.rect.center = x, y
        self.dirty = 2

    def resize(self, w, h):
        self.m_size = w, h
        self.repaint()

    def repaint(self):
        self._updateImage() # this only updates the surface.
        self.dirty = 2      # this only makes the screen get drawn the
                            # current surface in the next update.

    def update(self, dt):
        pass

    def setAngle(self, angle):
        if self._imageCache is None:
            self._imageCache = self.image
        self.image = pygame.transform.rotate(self._imageCache, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.m_position
        self.m_angle = angle
        self.dirty = 2

    def free(self):
        self._imageCache = None