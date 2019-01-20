from core.actor import SimulationActor
from core.debug_drawing import DebugDrawing
from pygame.math import Vector2
import core.colors as colors
import math

class Dycicle(SimulationActor):
    """Vehicle with two wheels (left and right) with a number of antennas
    regulary distributed"""
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

