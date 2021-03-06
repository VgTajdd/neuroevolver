## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## simulation_screen.py                                                      ##
## ========================================================================= ##

import pygame
from core.screen_base import ScreenBase
from enums import ScreenType, SimulationType
from core.simulation_base import SimulationBase
from core.hud_base import HudBase
from core.debug_drawing import DebugDrawing
import settings

class SimulationScreen(ScreenBase):
    def __init__(self, width, height, color):
        self.m_simulation = None
        self.m_hud = None
        self.m_debugContainer = []
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.SIMULATION

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
        dirtyRectsDebug = []
        if settings.SHOW_DEBUG_SHAPES:
            self.m_simulation.debugDraw(screen)
            self.m_debugContainer = self.m_simulation.m_debugContainer.copy()
            dirtyRectsDebug = DebugDrawing.draw(self.m_debugContainer, screen)
            self.m_debugContainer.clear()
            #self.m_simulation.debugDraw(screen)
        return dirtyRectsSim + dirtyRectsHud + dirtyRectsDebug

    def updateTime(self, dt):
        limited_dt = dt
        if dt > 100:
            limited_dt = 100
        self.m_hud.updateTime(limited_dt)
        self.m_simulation.update(limited_dt)

    def onMouseMove(self, event):
        self.m_hud.onMouseMove(event)
        if self.m_simulation and self.m_simulation.m_mouseInputsEnabled:
            self.m_simulation.onMouseMove(event)

    def onMouseDown(self, event):
        self.m_hud.onMouseDown(event)
        if self.m_simulation and self.m_simulation.m_mouseInputsEnabled:
            self.m_simulation.onMouseDown(event)

    def onMouseRelease(self, event):
        self.m_hud.onMouseRelease(event)
        if self.m_simulation and self.m_simulation.m_mouseInputsEnabled:
            self.m_simulation.onMouseRelease(event)

    def onKeyPress(self, event):
        if self.m_simulation and self.m_simulation.m_keyboardInputsEnabled:
            self.m_simulation.onKeyPress(event)

    def onKeyRelease(self, event):
        if self.m_simulation and self.m_simulation.m_keyboardInputsEnabled:
            self.m_simulation.onKeyRelease(event)

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