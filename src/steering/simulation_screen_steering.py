from core.simulation_screen import SimulationScreen
from steering.simulation_steering import SimulationSteering
from steering.hud_steering import HudSteering

class SimulationScreenSteering(SimulationScreen):
    def __init__(self, width, height, color):
        SimulationScreen.__init__(self, width, height, color)

    def createSimulation(self):
        self.m_simulation = SimulationSteering(self, self.m_width, self.m_height)

    def createHud(self):
        self.m_hud = HudSteering(self.m_width, self.m_height)