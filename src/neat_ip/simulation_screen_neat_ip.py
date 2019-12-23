## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## simulation_screen_neat_ip.py                                              ##
## ========================================================================= ##

from core.simulation_screen import SimulationScreen
from neat_ip.hud_neat_ip import HudNeatIP
from neat_ip.simulation_neat_ip import SimulationNeatIP

class SimulationScreenNeatIP(SimulationScreen):
    def __init__(self, width, height, color, params):
        self.params = params
        SimulationScreen.__init__(self, width, height, color)

    def createSimulation(self):
        self.m_simulation = SimulationNeatIP(self, self.m_width, self.m_height, self.params)

    def createHud(self):
        self.m_hud = HudNeatIP(self.m_width, self.m_height, self.params)