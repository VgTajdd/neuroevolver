from actor import Actor
from pygame.math import Vector2
import colors

class ActorSteering(Actor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        Actor.__init__(self, pos, size, color, imagePath, alpha, layer)

        # Movement vars
        self.m_maxSpeed = 4.0
        self.m_maxForce = 0.1
        self.m_velocity = Vector2(-1,-10)
        self.m_acceleration = Vector2()
        self.m_target = Vector2(200, 200)

        self.m_imageDirection = Vector2(0,-1)

    def updateMovement(self, dt):
        # Update velocity
        self.m_velocity = (self.m_velocity + self.m_acceleration)
        # Limit speed
        if self.m_velocity.length() > self.m_maxSpeed:
            self.m_velocity.scale_to_length(self.m_maxSpeed)
        x = self.m_position[0] + self.m_velocity.x
        y = self.m_position[1] + self.m_velocity.y
        self.setPosition(x, y);
        # Reset accelerationelertion to 0 each cycle
        if self.m_acceleration.length() > 0.001:
            self.m_acceleration.scale_to_length(0);

    def seek(self):
        desired = self.m_target - self.m_position
        #desired.scale_to_length(self.m_maxSpeed)
        steer = desired - self.m_velocity
        if steer.length() > self.m_maxForce:
            steer.scale_to_length(self.m_maxForce)
        self.applyForce(steer)

    def update(self, dt):
        self.seek()
        self.updateMovement(dt)
        self.setAngle(self.m_velocity.angle_to(self.m_imageDirection))

    def applyForce(self, force):
        self.m_acceleration = self.m_acceleration + force