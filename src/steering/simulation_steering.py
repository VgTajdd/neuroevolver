from core.simulation_base import SimulationBase
from steering.actor_steering import ActorSteering
from core.actor import Actor
from enums import SteeringBehaviourType
from core.simulation_base import SimulationActor
import core.colors as colors
import math

class SimulationSteering(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)

        self.m_body = None
        self.m_angle = -0.3
        self.m_velocity = 0
        self.m_acceleration = 0
        self.m_g = 9.8
        self.m_l = 1

        self.init()

    def init(self):
        targetActor = SimulationActor((400, 300), (20, 20), color = colors.BLUE)
        self.addActor(targetActor)

        #self.addActor(SimulationActor((400, 300), (40, 40), imagePath = "assets/imageqt.png"))
        #self.addActor(ActorSteering((0, 150), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((100, 100), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((500, 100), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((333, 100), (10, 20), imagePath = "assets/actor0.png", layer = 2))
        #self.addActor(ActorSteering((750, 550), (10, 20), imagePath = "assets/actor0.png", layer = 2))

        actor = ActorSteering((750, 500), (10, 20), imagePath = "assets/actor0.png", layer = 2)
        actor.addSteeringComponent(SteeringBehaviourType.SEEK, targetActor)
        self.addActor(actor)

        actor2 = ActorSteering((100, 100), (10, 20), imagePath = "assets/actor1.png", layer = 2)
        actor2.addSteeringComponent(SteeringBehaviourType.SEEK, targetActor)
        #actor2.addSteeringComponent(SteeringBehaviourType.SEEK, actor)
        self.addActor(actor2)

        self.m_body = self.addActor(SimulationActor((100, 100), (10, 100), rc = (5,0)))

    def update(self, dt):
        super().update(dt)
        dt_secs = dt/1000
        self.m_acceleration = -(self.m_g/self.m_l)*math.sin(self.m_angle)
        self.m_velocity += self.m_acceleration*dt_secs
        self.m_angle += self.m_velocity*dt_secs
        #print(self.m_angle)
        self.m_body.setAngle(self.m_angle*180.0/math.pi)
