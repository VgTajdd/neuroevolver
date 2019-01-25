from core.actor import SimulationActor
import core.colors as colors
from Box2D import b2Vec2, b2_pi
import settings

class ActorB2D(SimulationActor):
    """description of class"""
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer)
        self.m_body = None
        self.PPM = 20 # pixels per meter

    def update(self, dt):
        self.setPosition(self.m_body.position[0] * self.PPM,
                         settings.APP_HEIGHT - self.m_body.position[1] * self.PPM)
        self.setAngle(self.m_body.transform.angle * 180.00 / b2_pi)
        return super().update(dt)

    def free(self):
        self.m_body = None
        return super().free()