from core.simulation_base import SimulationActor
import core.colors as colors
import math

class SimplePendulum(SimulationActor):
    """Pendulum simple actor class"""
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1, rc = None):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer, rc)

        # Constants.
        self.m_l = 1
        self.m_g = 9.8
        self.m_pi_180 = math.pi/180.0

        # Initial position.
        self.m_angle = -60
        self.m_pi_180 = math.pi/180.0

        # Rotation vars in radians.
        self.m_angleInRadians = self.m_angle * self.m_pi_180
        self.m_angularVelocity = 0
        self.m_angularAcceleration = 0

    def update(self, dt):
        super().update(dt)
        dt_secs = dt/1000

        # All this update in radians.
        self.m_angularAcceleration = -(self.m_g/self.m_l) * math.sin(self.m_angleInRadians)
        self.m_angularVelocity += self.m_angularAcceleration * dt_secs
        self.m_angleInRadians += self.m_angularVelocity * dt_secs

        # Transfrom to sexagesimals.
        self.setAngle(self.m_angleInRadians/self.m_pi_180) #print(self.m_angle)