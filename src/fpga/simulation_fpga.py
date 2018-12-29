from core.simulation_base import SimulationBase

class SimulationFPGA(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.m_foodActors = []
        self.m_poisonActors = []
        self.m_fpVehicles = []
        self.m_totalFood = 100
        self.m_totalPoison = 100
        self.init()

    def init(self):
        pass

    def free(self):
        pass