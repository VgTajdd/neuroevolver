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

    def init(self):
        self.createSimulation()
        self.createHud()

    def createSimulation(self):
        self.m_simulation = SimulationBase(self, self.m_width, self.m_height)

    def createHud(self):
        self.m_hud = HudBase(self.m_width, self.m_height)