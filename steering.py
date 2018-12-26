from pygame.math import Vector2

class Steering():

    def pursuit(actor, targetActor, steeringConstant, T = 200): # T : ms
        futurePosition = targetActor.m_position + targetActor.m_velocity * T
        Steering.seek(actor, futurePosition, steeringConstant)

    def evade(actor, targetActor, steeringConstant, T = 200): # T : ms
        futurePosition = targetActor.m_position + targetActor.m_velocity * T
        Steering.flee(actor, futurePosition, steeringConstant)

    def seek(actor, target, steeringConstant):
        Steering.steer(actor, target, steeringConstant)

    def flee(actor, target, steeringConstant):
        Steering.steer(actor, target, -steeringConstant)

    def steer(actor, target, steeringConstant):
        # Desired.
        desired_velocity = target - Vector2(actor.m_position)   # direction
        if desired_velocity.length() <= 0.001: return           # non-zero desired
        desired_velocity.scale_to_length(actor.m_maxSpeed)      # desired velocity

        # Steering force: Force = costant * speed.
        steer = steeringConstant * (desired_velocity - actor.m_velocity)

        ## Truncating steering force.
        #if steer.length() > actor.m_maxForce:
        #    steer.scale_to_length(actor.m_maxForce)

        actor.applyForce(steer)
