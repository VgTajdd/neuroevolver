from simulation_base import SimulationBase
from actor_steering import ActorSteering
from enums import SteeringBehaviourType
from actor import Actor
import colors

class SimulationSteering(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.init()

    def init(self):
        targetActor = Actor((400, 300), (20, 20), color = colors.BLUE)
        self.addActor(targetActor)
        #self.addActor(Actor((400, 300), (40, 40), imagePath = "assets/imageqt.png"))
        #self.addActor(ActorSteering((0, 150), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((100, 100), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((500, 100), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((333, 100), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((750, 550), (10, 20), imagePath = "assets/actor0.png", layer = 2))

        actor = ActorSteering((750, 500), (10, 20), imagePath = "assets/actor0.png", layer = 2)
        actor.addSteeringComponent(SteeringBehaviourType.SEEK, targetActor)
        self.addActor(actor)

