from core.simulation_screen import SimulationScreen
from b2d.simulation_b2d import SimulationB2D
from b2d.simulation_b2d_dip import SimulationB2DDIP
from b2d.hud_b2d import HudB2D

class SimulationScreenB2D(SimulationScreen):
    def __init__(self, width, height, color, params):
        self.params = params
        SimulationScreen.__init__(self, width, height, color)

    def createSimulation(self):
        #self.m_simulation = SimulationB2D(self, self.m_width, self.m_height)
        self.m_simulation = SimulationB2DDIP(self, self.m_width, self.m_height, self.params)

    def createHud(self):
        self.m_hud = HudB2D(self.m_width, self.m_height)