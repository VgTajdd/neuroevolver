import pygame
from enums import ScreenType
from control import Control
from control import Button

class ScreenBase(pygame.sprite.LayeredDirty):
    def __init__(self, width, height, color):
        pygame.sprite.LayeredDirty.__init__(self)
        self.m_type = ScreenType.DEFAULT
        self.m_controls = []
        self.m_height = height
        self.m_width = width
        self.m_color = color
        self.init()

    def addControl(self, control):
        self.add(control)
        self.m_controls.append(control)

    def init(self):
        pass

    def draw(self, screen):
        screen.fill(self.m_color)
        return super().draw(screen) #same as down but it doesn't need 'self'
        #return pygame.sprite.LayeredDirty.draw(self, screen);

    def updateTime(self, dt):
        for control in self.m_controls:
            control.updateTime(dt)

    def onKeyPress(self, key):
        pass

    def onMouseMove(self, event):
        for control in self.m_controls:
            if control.mouseEventsEnabled():
                control.onMouseMove(event)

    def onMouseDown(self, event):
        for control in self.m_controls:
            if control.mouseEventsEnabled():
                control.onMouseDown(event)

    def onMouseRelease(self, event):
        for control in self.m_controls:
            if control.mouseEventsEnabled():
                control.onMouseRelease(event)