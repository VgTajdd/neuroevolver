from core.actor import SimulationActor
import core.colors as colors
from Box2D import b2Vec2, b2_pi
import settings

class ActorB2D(SimulationActor):
    """description of class"""
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer)
        self.m_body = None
        self.m_lastPosition = None
        self.m_lastAngle = None
        self.m_speed = 0, 0
        self.m_rotSpeed = 0

    def update(self, dt):
        self.setPosition(self.m_body.position[0] * settings.B2D_PPM,
                         settings.APP_HEIGHT - self.m_body.position[1] * settings.B2D_PPM)
        self.setAngle(self.m_body.transform.angle * 180.00 / b2_pi)
        if self.m_lastPosition and self.m_lastAngle:
            self.m_speed = (self.m_position - self.m_lastPosition)/(dt/1000)
            self.m_rotSpeed = (self.m_angle - self.m_lastAngle)/(dt/1000)
        self.m_lastAngle = self.m_angle
        self.m_lastPosition = self.m_position
        return super().update(dt)

    def free(self):
        self.m_body = None
        return super().free()