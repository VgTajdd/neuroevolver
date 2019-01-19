from core.simulation_base import SimulationBase
from core.actor import DraggableActor, SimulationActor
from core.debug_drawing import DebugDrawing
from steering.actor_steering import ActorSteering
from physics.simple_pendulum import SimplePendulum
from physics.inverted_pendulum import InvertedPendulum
from enums import SteeringBehaviourType
import core.colors as colors
from pygame.math import Vector2
import math

class SimulationSteering(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.m_invertedPendulum = None
        self.m_target = None
        self.m_vehicle = None
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

        self.m_vehicle = Vehicle((400, 500), (20, 20), imagePath = "assets/actor0.png", layer = 2)
        self.addActor(self.m_vehicle)

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

    def update(self, dt):
        super().update(dt)
        self.m_debugContainer += self.m_vehicle.m_debugShapes

class Vehicle(SimulationActor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer)

        self.m_speedL = 50 # pixels/s
        self.m_speedR = 20 # pixels/s
        self.m_wheelDistance = 20 # pixeles
        self.m_angle = 10

        self.m_antennaLength = 50
        self.m_antennaRange = 60
        self.m_antenasQuantity = 5
        self.m_antennas = [Vector2(0, -self.m_antennaLength) for i in range(self.m_antenasQuantity)]
        [self.setupAntenna(i) for i in range(self.m_antenasQuantity)]

    def update(self, dt):
        super().update(dt)
        dt_seconds = dt/1000 # seconds
        angularSpeed = (self.m_speedR - self.m_speedL)/(self.m_wheelDistance) # rad/s
        angle_delta = angularSpeed*dt_seconds*180/math.pi
        self.setAngle(self.m_angle + angle_delta)
        delta = Vector2(0, -(dt_seconds*(self.m_speedL + self.m_speedR)/2))
        delta = delta.rotate(-self.m_angle)
        self.setPosition(self.m_position + delta)
        [self.updateAntenna(i, angle_delta) for i in range(self.m_antenasQuantity)]

    def setupAntenna(self, index):
        delta = self.m_antennaRange/(self.m_antenasQuantity - 1)
        angle = self.m_angle + (-self.m_antennaRange/2) + index*delta
        self.m_antennas[index] = self.m_antennas[index].rotate(-angle)

    def updateAntenna(self, index, angle_delta):
        self.m_antennas[index] = self.m_antennas[index].rotate(-angle_delta)
        self.addDebugShape(DebugDrawing.line(colors.GREEN, self.m_position, self.m_position + self.m_antennas[index]))

