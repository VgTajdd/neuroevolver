from core.simulation_base import SimulationBase
from steering.actor_steering import ActorSteering
from enums import SteeringBehaviourType
from core.simulation_base import SimulationActor
from physics.simple_pendulum import SimplePendulum
import core.colors as colors

class SimulationSteering(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.init()

    def init(self):
        targetActor = SimulationActor((400, 300), (20, 20), color = colors.BLUE)
        self.addActor(targetActor)

        actor = ActorSteering((750, 500), (10, 20), imagePath = "assets/actor0.png", layer = 2)
        actor.addSteeringComponent(SteeringBehaviourType.SEEK, targetActor)
        self.addActor(actor)

        actor2 = ActorSteering((100, 100), (10, 20), imagePath = "assets/actor1.png", layer = 2)
        actor2.addSteeringComponent(SteeringBehaviourType.SEEK, targetActor)
        #actor2.addSteeringComponent(SteeringBehaviourType.SEEK, actor)
        self.addActor(actor2)

        # Added simple pendulum.
        self.addActor(SimplePendulum((100, 100), (10, 100), rc = (5,0)))
