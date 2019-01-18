from core.actor import SimulationActor
import core.colors as colors
import math
import numpy as np
import pygame

class InvertedPendulum(SimulationActor):
    """Pendulum simple actor class"""
    def __init__(self, pos, size, color = colors.RED, imagePath = '', alpha = 255, layer = 1, rc = None):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer, rc)

        # Constants.
        self.l = 1      # m
        self.g = 9.8    # m/s2
        self.pi_180 = math.pi/180.0
        self.m = 0.1    # kg
        self.M = 0.5    # kg

        # Initial position.
        self.m_angle = -20
        self.m_xM = self.m_position.x       # pixels

        # Rotation vars in radians.
        self.m_angleInRadians = self.m_angle * self.pi_180
        self.m_angularVelocity = 0          # rad/s
        self.m_angularAcceleration = 0      # rad/s2

        # Traslation vars in meters.
        self.m_speedM = 0                   # m/s
        self.m_horizontalAcceleration = 0   # m/s2

        # Car actor.
        self.m_carActor = SimulationActor(pos, (50, 20), color = colors.BLUE, rc = (25, 0))

        # Input.
        self.u = 0      # N = kg*m/s2

    def update(self, dt):
        super().update(dt)
        dt_secs = dt/1000

        # Calculating accelerations.
        ml = self.m * self.l
        _cos = math.cos(self.m_angleInRadians)
        _sin = math.sin(self.m_angleInRadians)
        _as_sq = self.m_angularVelocity * self.m_angularVelocity
        a = [[ml, self.m * _cos], [ml * _cos, self.m + self.M]]
        b = [[self.m * self.g * _sin], [self.u + (ml * _as_sq * _sin)]]
        t = np.linalg.inv(np.array(a)).dot(np.array(b))
        self.m_angularAcceleration = t[0][0]        # rad/s2
        self.m_horizontalAcceleration = t[1][0]     # m/s2

        # Updating motion vars.
        self.m_speedM += self.m_horizontalAcceleration * dt_secs
        delta_meters = self.m_speedM * dt_secs      # m
        self.m_xM += delta_meters * 100             # 1pixel = 1cm = 0.01m
        self.m_angularVelocity += self.m_angularAcceleration * dt_secs
        self.m_angleInRadians += self.m_angularVelocity * dt_secs

        # Updating position.
        self.m_position.x = self.m_xM
        self.m_carActor.setPosition(self.m_position)

        # Transfrom to sexagesimals. Updating angle.
        self.setAngle(-self.m_angleInRadians/self.pi_180)

    def onKeyPress(self, event):
        if event == pygame.K_LEFT:
            self.u = -5
        elif event == pygame.K_RIGHT:
            self.u = 5

    def onKeyRelease(self, event):
        if event == pygame.K_LEFT:
            self.u = 0
        elif event == pygame.K_RIGHT:
            self.u = 0

    def addToSimulation(self, simulation):
        simulation.addActor(self)
        simulation.addActor(self.m_carActor)

    def removeFromSimulation(self, simulation):
        simulation.removeActor(self)
        simulation.removeActor(self.m_carActor)
