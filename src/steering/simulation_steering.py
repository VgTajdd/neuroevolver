from core.simulation_base import SimulationBase
from core.actor import DraggableActor
from steering.actor_steering import ActorSteering
from physics.simple_pendulum import SimplePendulum
from physics.inverted_pendulum import InvertedPendulum
from enums import SteeringBehaviourType
import core.colors as colors

class SimulationSteering(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.m_invertedPendulum = None
        self.m_target = None
        self.init()

    def init(self):
        self.m_target = DraggableActor((400, 300), (20, 20), color = colors.BLUE)
        self.addActor(self.m_target)

        actor = ActorSteering((750, 500), (10, 20), imagePath = "assets/actor0.png", layer = 2)
        actor.addSteeringComponent(SteeringBehaviourType.SEEK, self.m_target)
        self.addActor(actor)

        actor2 = ActorSteering((100, 100), (10, 20), imagePath = "assets/actor1.png", layer = 2)
        actor2.addSteeringComponent(SteeringBehaviourType.SEEK, self.m_target)
        self.addActor(actor2)

        # Added simple pendulum.
        self.addActor(SimplePendulum((100, 100), (10, 100), rc = (5, 0)))

        # Added inverted pendulum.
        self.m_invertedPendulum = InvertedPendulum((500, 100), (10, 100), rc = (5, 100), layer = 2)
        self.m_invertedPendulum.addToSimulation(self)

    def onKeyPress(self, event):
        self.m_invertedPendulum.onKeyPress(event)

    def onKeyRelease(self, event):
        self.m_invertedPendulum.onKeyRelease(event)

    def onMouseMove(self, event):
        if self.m_target:
            self.m_target.onMouseMove(event)

    def onMouseDown(self, event):
        if self.m_target:
            self.m_target.onMouseDown(event)

    def onMouseRelease(self, event):
        if self.m_target:
            self.m_target.onMouseRelease(event)
