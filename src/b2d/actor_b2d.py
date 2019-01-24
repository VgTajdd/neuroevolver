from core.actor import SimulationActor
import core.colors as colors
import settings

class ActorB2D(SimulationActor):
    """description of class"""
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        SimulationActor.__init__(self, pos, size, color, imagePath, alpha, layer)
        self.m_body = None

    def update(self, dt):
        self.setPosition(self.m_body.position[0],
                         settings.APP_HEIGHT - self.m_body.position[1])
        self.setAngle(self.m_body.angle)
        return super().update(dt)