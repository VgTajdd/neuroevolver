from core.simulation_screen import SimulationScreen
from b2d.simulation_b2d import SimulationB2D
from b2d.simulation_b2d_dip import SimulationB2DDIP
from b2d.simulation_b2d_walker import SimulationB2DWalker
from b2d.simulation_b2d_tip import SimulationB2DTIP
from b2d.hud_b2d import HudB2D, HudB2DNEATDIP, HudB2DNEATWalker, HudB2DNEATTIP
from enums import SimulationType

class SimulationScreenB2D(SimulationScreen):
    def __init__(self, width, height, color, params):
        self.params = params
        self.m_simulationType = SimulationType.B2D
        if self.params and self.params['simulationType']:
            self.m_simulationType = self.params['simulationType']
        SimulationScreen.__init__(self, width, height, color)

    def createSimulation(self):
        if self.m_simulationType is SimulationType.NEAT_B2D_DIP:
            self.m_simulation = SimulationB2DDIP(self, self.m_width, self.m_height, self.params)
        elif self.m_simulationType is SimulationType.NEAT_B2D_TIP:
            self.m_simulation = SimulationB2DTIP(self, self.m_width, self.m_height, self.params)
        elif self.m_simulationType is SimulationType.NEAT_B2D_WALKER:
            self.m_simulation = SimulationB2DWalker(self, self.m_width, self.m_height, self.params)
        else:
            self.m_simulation = SimulationB2D(self, self.m_width, self.m_height)

    def createHud(self):
        if self.m_simulationType is SimulationType.NEAT_B2D_DIP:
            self.m_hud = HudB2DNEATDIP(self.m_width, self.m_height, self.params)
        elif self.m_simulationType is SimulationType.NEAT_B2D_TIP:
            self.m_hud = HudB2DNEATTIP(self.m_width, self.m_height, self.params)
        elif self.m_simulationType is SimulationType.NEAT_B2D_WALKER:
            self.m_hud = HudB2DNEATWalker(self.m_width, self.m_height, self.params)
        else:
            self.m_hud = HudB2D(self.m_width, self.m_height)