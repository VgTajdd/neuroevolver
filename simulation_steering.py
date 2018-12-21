from simulation_base import SimulationBase
from actor_steering import ActorSteering

class SimulationSteering(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.init()

    def init(self):
        self.addActor(ActorSteering((100,100), (50, 50), imagePath = "assets/actor0.png"));
