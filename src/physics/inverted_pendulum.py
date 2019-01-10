from core.simulation_base import SimulationActor
import core.colors as colors
import math
import numpy as np

class InvertedPendulum(SimulationActor):
    """Pendulum simple actor class"""
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1, rc = None):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer, rc)

        # Constants.
        self.m_l = 1
        self.m_g = 9.8
        self.m_pi_180 = math.pi/180.0
        self.m_m = 1
        self.m_M = 5

        # Initial position.
        self.m_angle = -60
        self.m_pi_180 = math.pi/180.0
        self.m_xM = self.m_position.x

        # Rotation vars in radians.
        self.m_angleInRadians = self.m_angle * self.m_pi_180
        self.m_angularVelocity = 0
        self.m_angularAcceleration = 0

        # Traslation vars in meters.
        self.m_speedM = 0
        self.m_accelerationM = 0

    def update(self, dt):
        super().update(dt)
        dt_secs = dt/1000

        u = 0
        ml = self.m_m*self.m_l
        _cos = math.cos(self.m_angleInRadians)
        _sin = math.sin(self.m_angleInRadians)
        _as_sq = self.m_angularVelocity*self.m_angularVelocity
        a = [[ml,self.m_m*_cos],[ml*_cos,self.m_m+self.m_M]]
        b = [[self.m_m*self.m_g],[u+(ml*_as_sq*_sin)]]

        t = np.linalg.inv(np.array(a)).dot(np.array(b))

        self.m_angularAcceleration = t[0][0]
        self.m_accelerationM = t[1][0]

        self.m_speedM += self.m_accelerationM * dt_secs
        self.m_xM += self.m_speedM * dt_secs

        self.m_angularVelocity += self.m_angularAcceleration * dt_secs
        self.m_angleInRadians += self.m_angularVelocity * dt_secs

        print(self.m_xM)

        # Transfrom to sexagesimals.
        self.setAngle(self.m_angleInRadians/self.m_pi_180) #print(self.m_angle)