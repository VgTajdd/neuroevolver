from core.simulation_base import SimulationBase
from core.actor import DraggableActor, SimulationActor
from steering.actor_steering import ActorSteering
from physics.simple_pendulum import SimplePendulum
from physics.inverted_pendulum import InvertedPendulum
from enums import SteeringBehaviourType
import core.colors as colors
from pygame.math import Vector2

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

        vehicle = Vehicle((400, 500), (25, 35), imagePath = "assets/actor0.png", layer = 2)
        self.addActor(vehicle)

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

class Vehicle(SimulationActor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer)

        self.m_speedL = 0.15
        self.m_speedR = 0.2
        self.m_radius = 0.1 # 10cm = 10 pixeles
        self.m_angle = 10

    def update(self, dt):
        #dt_seconds = dt/1000 # TOFIX, also in steering demo(speeds and dt).
        angularSpeed = (self.m_speedR - self.m_speedL)/(2*self.m_radius)
        self.setAngle(self.m_angle + angularSpeed*dt)
        delta = Vector2(0, -(dt*(self.m_speedL + self.m_speedR)/2))
        delta = delta.rotate(-self.m_angle)
        self.setPosition(self.m_position + delta)
        super().update(dt)
