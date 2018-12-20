import pygame
from screen_base import ScreenBase
from enums import ScreenType
from simulation_base import SimulationBase
from hud_base import HudBase

class SimulationScreen(ScreenBase):
    def __init__(self, width, height, color):
        self.m_simulation = None
        self.m_hud = None
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
        dirtyRectsA = pygame.sprite.LayeredDirty.draw(self.m_hud, screen)
        dirtyRectsB = self.m_simulation.draw(screen)
        return dirtyRectsA + dirtyRectsB

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
        self.m_hud.free()