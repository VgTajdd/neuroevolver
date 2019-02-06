from b2d.actor_b2d import ActorB2D
from b2d.simulation_b2d import SimulationB2D
from Box2D import b2_pi
import settings
import pygame
import neat
import pickle

class SimulationB2DWalker(SimulationB2D):
    def __init__(self, container, width, height, params):
        #self.m_keyboardInputsEnabled = False
        SimulationB2D.__init__(self, container, width, height)

        Walker(self);

        #self.m_isTraining = False
        #if 'genomes' in params and 'config' in params:
        #    self.initParams(params['genomes'], params['config'])
        #    self.m_isTraining = True
        #else:
        #    config = neat.Config(
        #        neat.DefaultGenome,
        #        neat.DefaultReproduction,
        #        neat.DefaultSpeciesSet,
        #        neat.DefaultStagnation,
        #        'config_neat_dip')
        #    genome = pickle.load(open('winner_neat_dip.pkl', 'rb'))
        #    self.initParams([genome], config)

    def initParams(self, genomes, config):
        self.m_systems = [NNDIPSystem(self, genome, config) for genome in genomes]

    #def update(self, dt):
    #    if len(self.m_systems) == 0:
    #        return

    #    for system in self.m_systems:
    #        if not system.m_isAlive:
    #            self.m_systems.remove(system)
    #            system.free()
    #            continue
    #        system.update(dt)

    #    if len(self.m_systems) == 0:
    #        my_event = pygame.event.Event(settings.NEAT_DIP_EVENT_END_TRAINING_STEP, message="Bad cat!")
    #        pygame.event.post(my_event)

    #    super().update(dt)

    def setupWorld(self):
        pass

    def init(self):
        actorGround = self.addActor(ActorB2D((400, 580), (800, 40)))
        self.m_groundBody = actorGround.m_body

class Walker(object):
    def __init__(self, simulation):
        self.m_simulation = simulation
        self.leftLeg = WalkerLeg(simulation)
        self.rightLeg = WalkerLeg(simulation)
        self.body = self.m_simulation.createSimpleBox((400, 325), (30, 30), settings.B2D_CAT_BITS_CAR)

        self.jL = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.body.m_body,
                                                       bodyB=self.leftLeg.upper.m_body,
                                                       localAnchorA=(0, 0),
                                                       localAnchorB=(0, 25/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=True,
                                                       lowerAngle=-10*b2_pi/180.0,
                                                       upperAngle=10*b2_pi/180.0)
        simulation.m_joints.append(self.jL)

        self.jR = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.body.m_body,
                                                       bodyB=self.rightLeg.upper.m_body,
                                                       localAnchorA=(0, 0),
                                                       localAnchorB=(0, 25/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=True,
                                                       lowerAngle=-10*b2_pi/180.0,
                                                       upperAngle=10*b2_pi/180.0)
        simulation.m_joints.append(self.jR)

    def free(self):
        self.m_simulation.m_b2dWorld.DestroyJoint(self.jL)
        self.m_simulation.m_joints.remove(self.jL)
        self.m_simulation.m_b2dWorld.DestroyJoint(self.jR)
        self.m_simulation.m_joints.remove(self.jR)
        self.m_simulation.m_b2dWorld.DestroyBody(self.body.m_body)
        self.m_simulation.removeActor(self.body)
        self.leftLeg.free()
        self.leftLeg = None
        self.rightLeg.free()
        self.rightLeg = None

class WalkerLeg(object):
    def __init__(self, simulation):
        self.m_simulation = simulation
        self.upper = self.m_simulation.createSimpleBox((400, 300), (10, 50), settings.B2D_CAT_BITS_BAR)
        self.lower = self.m_simulation.createSimpleBox((400, 250), (10, 50), settings.B2D_CAT_BITS_BAR)
        self.j = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.upper.m_body,
                                                       bodyB=self.lower.m_body,
                                                       localAnchorA=(0, -25/settings.B2D_PPM),
                                                       localAnchorB=(0, 25/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=True,
                                                       lowerAngle=0,
                                                       upperAngle=10*b2_pi/180.0)
        simulation.m_joints.append(self.j)

    def free(self):
        self.m_simulation.m_b2dWorld.DestroyJoint(self.j)
        self.m_simulation.m_joints.remove(self.j)
        self.m_simulation.m_b2dWorld.DestroyBody(self.upper.m_body)
        self.m_simulation.removeActor(self.upper)
        self.m_simulation.m_b2dWorld.DestroyBody(self.lower.m_body)
        self.m_simulation.removeActor(self.lower)