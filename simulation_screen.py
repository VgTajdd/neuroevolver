import pygame
from screen_base import ScreenBase
from enums import ScreenType

class SimulationScreen(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.SIMULATION