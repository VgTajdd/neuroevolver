import pygame
from core.screen_base import ScreenBase
from enums import ScreenType
from core.simulation_base import SimulationBase
from core.hud_base import HudBase

class SimulationScreen(ScreenBase):
    def __init__(self, width, height, color):
        self.m_simulation = None
        self.m_hud = None
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.SIMULATION
        self.m_debugContainer = []

    def setManager(self, manager):
        self.m_hud.setManager(manager)

    def init(self):
        self.createSimulation()
        self.createHud()

    def createSimulation(self):
        self.m_simulation = SimulationBase(self, self.m_width, self.m_height)

    def createHud(self):
        self.m_hud = HudBase(self.m_width, self.m_height)

    def draw(self, screen):
        screen.fill(self.m_color)
        # It's very important to respect this order of drawing because of those are differents
        # LayeredDirty classes and the only way to control that Hud is always on is this way.
        dirtyRectsSim = self.m_simulation.draw(screen)
        dirtyRectsHud = pygame.sprite.LayeredDirty.draw(self.m_hud, screen)
        self.m_debugContainer = self.m_simulation.m_debugContainer.copy()
        dirtyRectsDebug = DebugDrawing.draw(self.m_debugContainer, screen)
        self.m_debugContainer.clear()
        return dirtyRectsSim + dirtyRectsHud + dirtyRectsDebug

    def updateTime(self, dt):
        self.m_hud.updateTime(dt)
        self.m_simulation.updateTime(dt)

    def onMouseMove(self, event):
        self.m_hud.onMouseMove(event)

    def onMouseDown(self, event):
        self.m_hud.onMouseDown(event)

    def onMouseRelease(self, event):
        self.m_hud.onMouseRelease(event)

    def forceRedraw(self):
        self.m_hud.forceRedraw()
        self.m_simulation.forceRedraw()

    def free(self):
        self.m_simulation.free()
        self.m_simulation = None
        self.m_hud.free()
        self.m_hud = None
        self.m_debugContainer.clear()
        self.m_debugContainer = None

from enums import DebugShape

class DebugDrawing():
    def draw(list, screen):
        dirtyRects = []
        for obj in list:
            if 'shape' in obj:
                shape = obj['shape']
                if shape == DebugShape.LINE:
                    r = pygame.draw.line(screen, obj['c'], obj['sp'], obj['ep'], obj['w'])
                    dirtyRects.append(r)
                elif shape == DebugShape.RECT:
                    r = pygame.draw.rect(screen, obj['c'], obj['r'], obj['w'])
                    dirtyRects.append(r)
                elif shape == DebugShape.ELLIPSE:
                    r = pygame.draw.ellipse(screen, obj['c'], obj['r'], obj['w'])
                    dirtyRects.append(r)
        return dirtyRects

    def line(color, startPos, endPos, width = 1):
        obj = {}
        obj['c'] = color
        obj['shape'] = DebugShape.LINE
        obj['sp'] = startPos
        obj['ep'] = endPos
        obj['w'] = width
        return obj
    
    def ellipse(color, rect, width = 1):
        obj = {}
        obj['c'] = color
        obj['shape'] = DebugShape.ELLIPSE
        obj['r'] = rect
        obj['w'] = width
        return obj
    
    def rect(color, rect, width = 1):
        obj = {}
        obj['c'] = color
        obj['shape'] = DebugShape.RECT
        obj['r'] = rect
        obj['w'] = width
        return obj