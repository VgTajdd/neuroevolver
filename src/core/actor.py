## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## actor.py                                                                  ##
## ========================================================================= ##

import pygame
import core.colors as colors
from pygame.math import Vector2
import settings

class Actor(pygame.sprite.DirtySprite):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1, rc = None):
        pygame.sprite.DirtySprite.__init__(self)
        self.m_imagePath = imagePath
        self.m_size = size
        self.m_position = Vector2(pos) # positon of rotation center.

        relCenter = self.m_size[0] * 0.5, self.m_size[1] * 0.5

        self.m_rotationCenter = None # relative vector to rotation center.
        if rc is None:
            self.m_rotationCenter = relCenter
        elif type(rc) is tuple:
            self.m_rotationCenter = rc

        #self.m_origin = self.m_position - self.m_rotationCenter # topleft corner.
        self.m_offsetCenter = Vector2(relCenter) - self.m_rotationCenter

        self.m_color = color
        self.m_alpha = alpha
        self.m_supportAlpha = True

        # Rotation vars.
        self._imageCache = None
        self.m_angle = 0
        self._updateImage()
        self.visible = 1
        self._layer = layer
        self.dirty = 2

        # By default circle collision.
        self.radius = 5

        # Debug.
        self.m_debugShapes = []

    def _updateImage(self):
        if self.m_imagePath:
            if self.m_supportAlpha:
                if self.m_imagePath in settings.IMAGES_ALPHA and settings.IMAGES_ALPHA[self.m_imagePath]:
                    self.image = settings.IMAGES_ALPHA[self.m_imagePath].copy()
                else:
                    self.image = pygame.image.load(self.m_imagePath).convert_alpha()
                self.image.fill((255, 255, 255, self.m_alpha), None, pygame.BLEND_RGBA_MULT)
            else:
                if self.m_imagePath in settings.IMAGES and settings.IMAGES[self.m_imagePath]:
                    self.image = settings.IMAGES[self.m_imagePath].copy()
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
        self.rect.center = self.m_position + self.m_offsetCenter.rotate(-self.m_angle)

        if settings.SHOW_ACTOR_RECT:
            pygame.draw.rect(self.image, colors.RED, [0,0,self.rect.w, self.rect.h], 1)

        # Rotation.
        self._imageCache = None
        self.setAngle(self.m_angle)

        if settings.SHOW_ACTOR_RECT:
            pygame.draw.rect(self.image, colors.BLUE, [0,0,self.rect.w, self.rect.h], 1)

    def setImage(self, imagePath):
        self.m_imagePath = imagePath
        self.repaint()

    def setPosition(self, x_or_pair, y = None):
        x_input = 0
        y_input = 0
        if y == None:
            x_input = x_or_pair[0]
            y_input = x_or_pair[1]
        else:
            x_input = x_or_pair
            y_input = y
        self.m_position = Vector2(x_input, y_input)
        self.rect.center = self.m_position + self.m_offsetCenter.rotate(-self.m_angle)
        #self.dirty = 1

    def resize(self, w, h):
        self.m_size = w, h
        #self.m_origin = self.m_position - Vector2(self.m_rotationCenter)
        relCenter = self.m_size[0] * 0.5, self.m_size[1] * 0.5
        self.m_offsetCenter = Vector2(relCenter) - self.m_rotationCenter
        self.repaint()

    def repaint(self):
        self._updateImage() # this only updates the surface.
        #self.dirty = 1      # this only makes the screen get drawn the
                            # current surface in the next update.

    def update(self, dt):
        if settings.SHOW_DEBUG_SHAPES:
            self.m_debugShapes.clear()

    def setAngle(self, angle):
        if self._imageCache is None:
            self._imageCache = self.image.copy()

        self.image = pygame.transform.rotate(self._imageCache, angle)
        self.rect = self.image.get_rect()
        t = self.m_offsetCenter.rotate(-angle)
        self.rect.center = self.m_position + t

        self.m_angle = angle
        #self.dirty = 1

    def hasCircleCollisionWith(self, actor):
        return pygame.sprite.collide_circle(self, actor)

    def hasRectCollisionWith(self, actor):
        return pygame.sprite.collide_rect(self, actor)

    def free(self):
        self._imageCache = None
        if self.image:
            self.image.set_alpha(0) # forcing to hide.

        self.m_debugShapes.clear()
        self.m_debugShapes = None

    def addDebugShape(self, obj):
        if settings.SHOW_DEBUG_SHAPES:
            self.m_debugShapes.append(obj)

class SimulationActor(Actor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1, rc = None):
        Actor.__init__(self, pos, size, color, imagePath, alpha, layer, rc)
        self.m_health = 0
        self.m_state = 0
        self.m_isAwaitingToDelete = False

    def setAwaitingToDelete(self, value):
        self.m_isAwaitingToDelete = value

    def addHealth(self, hp):
        self.m_health += hp

class DraggableActor(SimulationActor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1, rc = None):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer, rc)
        self.m_isDraggable = True
        self.m_isInDrag = False
        self.m_lastMousePosition = None

    def onMouseMove(self, event):
        if not self.m_isDraggable:
            return
        if self.m_isInDrag:
            actualPos = event.pos
            delta = Vector2(actualPos) - self.m_lastMousePosition
            self.setPosition(self.m_position + delta)
            self.m_lastMousePosition = actualPos

    def onMouseDown(self, event):
        if not self.m_isDraggable:
            return
        if not self.m_isInDrag:
            if self.rect.collidepoint(event.pos):
                self.m_lastMousePosition = event.pos
                self.m_isInDrag = True

    def onMouseRelease(self, event):
        if not self.m_isDraggable:
            return
        self.m_isInDrag = False
        self.m_lastMousePosition = None