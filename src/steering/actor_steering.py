from core.actor import Actor
from pygame.math import Vector2
from enums import SteeringBehaviourType
from steering.steering_behaviour import SteeringBehaviour
import core.colors as colors

class ActorSteering(Actor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        Actor.__init__(self, pos, size, color, imagePath, alpha, layer)

        self.m_maxSpeed = 0.2
        self.m_behaviour = SteeringBehaviour(self)

        # Movement vars.
        self.m_velocity = Vector2(0.1, -0.1)
        self.m_acceleration = Vector2()
        self.m_mass = 1

        # Auxiliar vars.
        self.m_imageDirection = Vector2(0, -1)

    def addSteeringComponent(self, type, targetActor = None, targetPosition = None):
        self.m_behaviour.addComponent(type, targetActor, targetPosition)

    def updateMotion(self, dt):
        # Updating velocity.
        self.m_velocity += self.m_acceleration * dt

        # Limiting speed to max speed.
        if self.m_velocity.length() > self.m_maxSpeed:
            self.m_velocity.scale_to_length(self.m_maxSpeed)

        # Arriving.
        if self.m_behaviour.m_arriveEnabled:
            self.m_velocity.scale_to_length(self.m_maxSpeed * self.m_behaviour.m_arriveFactor)

        # Updating position.
        self.setPosition(self.m_position + self.m_velocity * dt)

        # Reseting acceleration to 0 each cycle.
        if self.m_acceleration.length() > 0.001:
            self.m_acceleration.scale_to_length(0)

    def update(self, dt):
        self.m_behaviour.update(dt)
        self.updateMotion(dt)
        # Update image direction.
        self.setAngle(self.m_velocity.angle_to(self.m_imageDirection))

    def applyForce(self, force):
        self.m_acceleration += (force / self.m_mass)

    def free(self):
        self.m_velocity = None
        self.m_acceleration = None
        self.m_imageDirection = None
        super().free();
