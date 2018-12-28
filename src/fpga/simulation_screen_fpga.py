from core.simulation_screen import SimulationScreen
from fpga.hud_fpga import HudFPGA
from fpga.simulation_fpga import SimulationFPGA

class SimulationScreenFPGA(SimulationScreen):
    def __init__(self, width, height, color):
        SimulationScreen.__init__(self, width, height, color)

    def createSimulation(self):
        self.m_simulation = SimulationFPGA(self, self.m_width, self.m_height)

    def createHud(self):
        self.m_hud = HudFPGA(self.m_width, self.m_height)