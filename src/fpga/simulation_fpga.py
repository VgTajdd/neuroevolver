from core.simulation_base import SimulationBase

class SimulationFPGA(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.init()

    def init(self):
        pass