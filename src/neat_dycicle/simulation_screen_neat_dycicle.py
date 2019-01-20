from core.simulation_screen import SimulationScreen
from neat_dycicle.hud_neat_dycicle import HudNeatDycicle
from neat_dycicle.simulation_neat_dycicle import SimulationNeatDycicle

class SimulationScreenNeatDycicle(SimulationScreen):
    def __init__(self, width, height, color, params):
        self.params = params
        SimulationScreen.__init__(self, width, height, color)

    def createSimulation(self):
        self.m_simulation = SimulationNeatDycicle(self, self.m_width, self.m_height, self.params)

    def createHud(self):
        self.m_hud = HudNeatDycicle(self.m_width, self.m_height, self.params)