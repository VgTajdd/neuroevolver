from actor import Actor
from pygame.math import Vector2
import colors

class ActorSteering(Actor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        Actor.__init__(self, pos, size, color, imagePath, alpha, layer)

        # Steering constants.
        self.m_maxSpeed = 0.2
        self.m_maxForce = 0.0001
        self.m_arriveEnabled = True
        self.m_arriveDistance = 50
        self.m_target = Vector2(200, 200)

        # Movement vars.
        self.m_velocity = Vector2(-1, -10)
        self.m_acceleration = Vector2()

        # Auxiliar vars.
        self.m_mass = 1
        self.m_imageDirection = Vector2(0, -1)

    def updateMovement(self, dt):
        # Updating velocity.
        self.m_velocity += self.m_acceleration * dt

        # Limiting speed to max speed.
        if self.m_velocity.length() > self.m_maxSpeed:
            self.m_velocity.scale_to_length(self.m_maxSpeed)

        # Arriving
        actualDistanceToTarget = self.m_target.distance_to(self.m_position)
        if 0.001 < actualDistanceToTarget < self.m_arriveDistance:
            self.m_velocity.scale_to_length(self.m_maxSpeed*actualDistanceToTarget/self.m_arriveDistance)

        # Updating position.
        self.setPosition(self.m_position + self.m_velocity * dt)

        # Reseting acceleratio to 0 each cycle.
        if self.m_arriveEnabled and self.m_acceleration.length() > 0.001:
            self.m_acceleration.scale_to_length(0)

    def seek(self):
        # Desired.
        desired = self.m_target - self.m_position # direction
        if desired.length() <= 0.001:
            return
        desired.scale_to_length(self.m_maxSpeed) # desired velocity

        # Steering force.
        steer = desired - self.m_velocity

        # Truncating steering force.
        if steer.length() > self.m_maxForce:
            steer.scale_to_length(self.m_maxForce)
        self.applyForce(steer)

    def update(self, dt):
        self.seek()
        self.updateMovement(dt)
        self.setAngle(self.m_velocity.angle_to(self.m_imageDirection))

    def applyForce(self, force):
        self.m_acceleration += (force / self.m_mass)