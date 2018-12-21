from actor import Actor
import colors

class ActorSteering(Actor):
    def __init__(self, pos, size, color = colors.WHITE, layer = 1):
        Actor.__init__(self, pos, size, color, layer)

    def update(self, dt):
        pass