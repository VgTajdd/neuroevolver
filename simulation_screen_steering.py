import pygame
from simulation_screen import SimulationScreen
from enums import ScreenType
from simulation_steering import SimulationSteering
from hud import Hud

class SimulationScreenSteering(SimulationScreen):
    def __init__(self, width, height, color):
        SimulationScreen.__init__(self, width, height, color)

    def createSimulation(self):
        self.m_simulation = SimulationSteering(self, self.m_width, self.m_height)

    def createHud(self):
        self.m_hud = Hud(self.m_width, self.m_height)