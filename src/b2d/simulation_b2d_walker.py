from b2d.actor_b2d import ActorB2D
from b2d.simulation_b2d import SimulationB2D
from Box2D import b2_pi
import settings
import pygame
import neat
import pickle
import math

class SimulationB2DWalker(SimulationB2D):
    def __init__(self, container, width, height, params):
        SimulationB2D.__init__(self, container, width, height)
        self.m_keyboardInputsEnabled = False
        self.m_mouseInputsEnabled = True

        #self.walker = Walker(self)

        self.m_isTraining = False
        if 'genomes' in params and 'config' in params:
            self.initParams(params['genomes'], params['config'])
            self.m_isTraining = True
            self.m_mouseInputsEnabled = False
        else:
            config = neat.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                'config_neat_walker')
            genome = pickle.load(open('winner_neat_walker.pkl', 'rb'))
            self.initParams([genome], config)

    def initParams(self, genomes, config):
        self.m_systems = [NNWalkerSystem(self, genome, config) for genome in genomes]

    def update(self, dt):
        if len(self.m_systems) == 0:
            return

        for system in self.m_systems:
            if not system.m_isAlive:
                self.m_systems.remove(system)
                system.free()
                continue
            system.update(dt)

        if len(self.m_systems) == 0:
            my_event = pygame.event.Event(settings.NEAT_WALKER_EVENT_END_TRAINING_STEP, message="Bad cat!")
            pygame.event.post(my_event)

        #print(self.walker.body.m_angle)
        #print(self.walker.jL.angle * 180/b2_pi)
        #self.walker.update(dt)
        super().update(dt)

    def setupWorld(self):
        pass

    def onMouseDown(self, event):
        #self.walker.changeFeet()
        super().onMouseDown(event)

    def init(self):
        actorGround = self.addActor(ActorB2D((400, 580), (800, 40)))
        self.m_groundBody = actorGround.m_body
        actorGround.m_body.fixtures[0].friction = 0.5

class NNWalkerSystem(object):
    """ Description of the class """
    def __init__(self, simulation, genome, config):
        self.m_simulationRef = simulation

        self.m_isAlive = True

        # Added walker.
        self.m_walker = Walker(simulation)

        self.m_neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
        self.m_genome = genome

        self.m_timeAlive = 0
        self.m_traveledDistance = 0

    def update(self, dt):

        if not self.m_isAlive:
            return

        self.m_walker.update(dt)

        inputAngleL = (((self.m_walker.jL.angle * 180/b2_pi) + 180) % 360) - 180 # [-180,180]
        inputAngleR = (((self.m_walker.jR.angle * 180/b2_pi) + 180) % 360) - 180 # [-180,180]
        inputAngleB = ((self.m_walker.body.m_angle + 180) % 360) - 180 # [-180,180]

        if self.m_simulationRef.m_isTraining:
            self.m_traveledDistance = self.m_walker.body.m_position.x - 100

            validTime = self.m_timeAlive < settings.NEAT_WALKER_MAX_TIME_ALIVE * 1000
            validAngle = abs(inputAngleB) < 70

            if not (validAngle and validTime):
                self.m_isAlive = False
                self.m_genome.fitness = max(0.0, self.m_walker.maxDistance)
                print('fitness: ' + str(self.m_genome.fitness))
                return

        inputAngleL = (((self.m_walker.jL.angle * 180/b2_pi) + 180) % 360) - 180 # [-180,180]
        inputAngleR = (((self.m_walker.jR.angle * 180/b2_pi) + 180) % 360) - 180 # [-180,180]
        inputAngleB = ((self.m_walker.body.m_angle + 180) % 360) - 180 # [-180,180]

        # Setup the input layer.
        #input = (abs(self.m_walker.lfootY-self.m_walker.rfootY),)
        #input = (abs(inputAngleL/180-inputAngleR/180),)
        #input = (inputAngleL/180,
        #         inputAngleR/180,
        #         inputAngleB/180)

        input = (abs(self.m_walker.lfootY-self.m_walker.rfootY),
                 self.m_walker.lfootY,
                 self.m_walker.rfootY)

        # Feed the neural network information.
        output = self.m_neuralNetwork.activate(input)

        # Obtain Prediction.
        if output[0] > 0.5:
            self.m_walker.changeFeet()

        self.m_timeAlive += dt

    def free(self):
        self.m_walker.free()
        self.m_walker = None
        self.m_simulationRef = None

class Walker(object):
    def __init__(self, simulation):
        self.m_simulation = simulation
        self.leftLeg = WalkerLeg(simulation)
        self.rightLeg = WalkerLeg(simulation)
        self.leftLeg.lower.m_body.fixtures[0].friction = 0.3
        self.rightLeg.lower.m_body.fixtures[0].friction = 0.3
        self.leftLeg.lower.m_body.fixtures[0].density = 1
        self.rightLeg.lower.m_body.fixtures[0].density = 1
        self.body = self.m_simulation.createSimpleBox((100, 525), (30, 30), settings.B2D_CAT_BITS_CAR)
        self.body.m_body.fixtures[0].density = 1

        self.jL = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.body.m_body,
                                                       bodyB=self.leftLeg.upper.m_body,
                                                       localAnchorA=(0, 0),
                                                       localAnchorB=(0, 25/settings.B2D_PPM),
                                                       enableMotor=True,
                                                       maxMotorTorque=1000,
                                                       enableLimit=True,
                                                       lowerAngle=-20*b2_pi/180.0,
                                                       upperAngle=20*b2_pi/180.0)
        simulation.m_joints.append(self.jL)

        self.jR = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.body.m_body,
                                                       bodyB=self.rightLeg.upper.m_body,
                                                       localAnchorA=(0, 0),
                                                       localAnchorB=(0, 25/settings.B2D_PPM),
                                                       enableMotor=True,
                                                       maxMotorTorque=1000,
                                                       enableLimit=True,
                                                       lowerAngle=-20*b2_pi/180.0,
                                                       upperAngle=20*b2_pi/180.0)
        simulation.m_joints.append(self.jR)

        #self.jL.motorSpeed = -1 # This makes walker move up the left leg.
        #self.leftLeg.j.lowerAngle = -20*b2_pi/180.0
        #self.leftLeg.j.upperAngle = 20*b2_pi/180.0

        #self.jR.motorSpeed = 1 # This makes walker move up the left leg.
        #self.rightLeg.j.lowerAngle = 0*b2_pi/180.0
        #self.rightLeg.j.upperAngle = 0*b2_pi/180.0

        self.m_left = True
        self.m_steps = 1
        self.m_stepScore = 0
        self.m_timeStep = 0

        self.lfootX = self.leftLeg.lower.m_position.x + 25*math.sin(math.pi*self.leftLeg.lower.m_angle/180.0)
        self.lfootY = self.leftLeg.lower.m_position.y + 25*math.cos(math.pi*self.leftLeg.lower.m_angle/180.0)
        self.rfootX = self.rightLeg.lower.m_position.x + 25*math.sin(math.pi*self.rightLeg.lower.m_angle/180.0)
        self.rfootY = self.rightLeg.lower.m_position.y + 25*math.cos(math.pi*self.rightLeg.lower.m_angle/180.0)

    def update(self, dt):
        self.m_timeStep += dt
        #print(self.leftLeg.lower.m_position, self.leftLeg.lower.m_angle)
        #print(self.leftLeg.lower.m_position.y + math.cos(math.pi*self.leftLeg.lower.m_angle/180.0))
        self.lfootX = self.leftLeg.lower.m_position.x + 25*math.sin(math.pi*self.leftLeg.lower.m_angle/180.0)
        self.lfootY = self.leftLeg.lower.m_position.y + 25*math.cos(math.pi*self.leftLeg.lower.m_angle/180.0)
        self.rfootX = self.rightLeg.lower.m_position.x + 25*math.sin(math.pi*self.rightLeg.lower.m_angle/180.0)
        self.rfootY = self.rightLeg.lower.m_position.y + 25*math.cos(math.pi*self.rightLeg.lower.m_angle/180.0)
        self.maxDistance = max(self.lfootX, self.rfootX)
        #print(self.maxDistance)

    def changeFeet(self):
        self.m_left = not self.m_left
        self.m_steps += 1

        self.m_stepScore += pow(self.m_timeStep/1000.0,2)
        self.m_timeStep = 0

        if self.m_left:
            self.jL.motorSpeed = -1 # This makes walker move up the left leg.
            self.leftLeg.j.lowerAngle = -20*b2_pi/180.0
            self.leftLeg.j.upperAngle = 20*b2_pi/180.0

            self.jR.motorSpeed = 1 # This makes walker move down the right leg.
            self.rightLeg.j.lowerAngle = 0*b2_pi/180.0
            self.rightLeg.j.upperAngle = 0*b2_pi/180.0
        else:
            self.jR.motorSpeed = -1
            self.rightLeg.j.lowerAngle = -20*b2_pi/180.0
            self.rightLeg.j.upperAngle = 20*b2_pi/180.0

            self.jL.motorSpeed = 1
            self.leftLeg.j.lowerAngle = 0*b2_pi/180.0
            self.leftLeg.j.upperAngle = 0*b2_pi/180.0

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
        self.upper = self.m_simulation.createSimpleBox((100, 500), (10, 50), settings.B2D_CAT_BITS_BAR)
        self.lower = self.m_simulation.createSimpleBox((100, 450), (10, 50), settings.B2D_CAT_BITS_BAR)
        self.j = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.upper.m_body,
                                                       bodyB=self.lower.m_body,
                                                       localAnchorA=(0, -25/settings.B2D_PPM),
                                                       localAnchorB=(0, 25/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=True,
                                                       lowerAngle=-20*b2_pi/180.0,
                                                       upperAngle=0)
        simulation.m_joints.append(self.j)

    def free(self):
        self.m_simulation.m_b2dWorld.DestroyJoint(self.j)
        self.m_simulation.m_joints.remove(self.j)
        self.m_simulation.m_b2dWorld.DestroyBody(self.upper.m_body)
        self.m_simulation.removeActor(self.upper)
        self.m_simulation.m_b2dWorld.DestroyBody(self.lower.m_body)
        self.m_simulation.removeActor(self.lower)