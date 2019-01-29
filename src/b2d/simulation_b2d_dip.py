from b2d.actor_b2d import ActorB2D
from b2d.simulation_b2d import SimulationB2D
from Box2D import b2AABB, b2Vec2, b2QueryCallback, b2_dynamicBody, b2Color, b2CircleShape, b2FixtureDef, b2BodyDef, b2PolygonShape, b2Filter
import settings
import pygame
import neat
import pickle

class SimulationB2DDIP(SimulationB2D):
    def __init__(self, container, width, height, params):
        self.m_keyboardInputsEnabled = False
        SimulationB2D.__init__(self, container, width, height)
        self.m_isTraining = False
        if 'genomes' in params and 'config' in params:
            self.init(params['genomes'], params['config'])
            self.m_isTraining = True
        else:
            config = neat.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                'config_neat_dip')
            genome = pickle.load(open('winner_neat_dip.pkl', 'rb'))
            self.init([genome], config)

    def init(self, genomes, config):
        super().init()
        self.m_systems = [NNDIPSystem(self, genome, config) for genome in genomes]

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
            my_event = pygame.event.Event(settings.NEATIP_EVENT_END_TRAINING_STEP, message="Bad cat!")
            pygame.event.post(my_event)

        super().update(dt)

    def setupWorld(self):
        pass

class NNDIPSystem(object):
    """ Description of the class """
    def __init__(self, simulation, genome, config):
        self.m_simulationRef = simulation

        self.m_isAlive = True

        # Added double inverted pendulum.
        self.m_dip = DIP(simulation)

        self.m_neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
        self.m_genome = genome

        self.m_timeAlive = 0
        self.m_traveledDistance = 0

    def update(self, dt):

        if not self.m_isAlive:
            return

        if self.m_simulationRef.m_isTraining:
            #self.m_traveledDistance += abs(self.m_invertedPendulum.m_speedM) * dt

            #validAngle = -settings.NEATIP_LIMIT_ANGLE < self.m_invertedPendulum.m_angle < settings.NEATIP_LIMIT_ANGLE
            #validPosition = 0 < self.m_invertedPendulum.m_position.x < settings.APP_WIDTH
            #validTime = self.m_timeAlive < settings.NEATIP_MAX_TIME_ALIVE * 1000

            if not (validAngle and validPosition and validTime):
                #deltaX = abs(settings.APP_WIDTH/2 - self.m_invertedPendulum.m_position.x)
                #print('fitness: ' + str(self.m_timeAlive) + ' ' + str(-self.m_traveledDistance/5) + ' ' + str(-deltaX*5) + ' ' + str(self.m_timeAlive - self.m_traveledDistance/5 - deltaX*5))
                #self.m_genome.fitness = max(0,self.m_timeAlive - self.m_traveledDistance/5 - deltaX*5)
                self.m_isAlive = False
                return

        #inputAngle = ((self.m_invertedPendulum.m_angle + 180) % 360) - 180 # [-180,180]

         # Setup the input layer
        #input = (inputAngle,
        #         self.m_invertedPendulum.m_angularVelocity,
        #         settings.APP_WIDTH/2 - self.m_invertedPendulum.m_position.x,
        #         self.m_invertedPendulum.m_speedM)

        # Feed the neural network information
        #output = self.m_neuralNetwork.activate(input)

        # Obtain Prediction
        #self.m_invertedPendulum.u = output[0]
        #f = self.box.m_body.GetWorldVector(localVector=(output[0], 0.0))
        #p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 0.0))
        #self.box.m_body.ApplyLinearImpulse(f, p, True)

        self.m_timeAlive += dt

    def free(self):
        #self.m_invertedPendulum.removeFromSimulation(self.m_simulationRef)
        #self.m_invertedPendulum = None
        self.m_dip.free()
        self.m_dip = None
        self.m_simulationRef = None

class DIP(object):
    def __init__(self, simulation):
        self.m_simulation = simulation
        self.box = self.createSimpleBox((400, 550), (40, 20))
        self.barA = self.createSimpleBox((400, 490), (10, 100))
        self.barB = self.createSimpleBox((400, 390), (10, 100))

        self.j1 = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.box.m_body,
                                                       bodyB=barA.m_body,
                                                       localAnchorA=(0, 0),
                                                       localAnchorB=(0, -50/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=False,
                                                       lowerAngle=0,
                                                       upperAngle=0)
        self.j2 = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=barA.m_body,
                                                       bodyB=barB.m_body,
                                                       localAnchorA=(0, 50/settings.B2D_PPM),
                                                       localAnchorB=(0, -50/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=False,
                                                       lowerAngle=0,
                                                       upperAngle=0)
        simulation.m_joints.append(self.j1)
        simulation.m_joints.append(self.j2)

    def createSimpleBox(self, screenBoxPosition, screenBoxSize):
        screenBoxWidth = screenBoxSize[0]
        screenBoxHeight = screenBoxSize[1]

        boxWidth = screenBoxWidth/settings.B2D_PPM
        boxHeight = screenBoxHeight/settings.B2D_PPM

        boxPosition = self.m_simulation.convertScreenToWorld(screenBoxPosition)

        shape = b2PolygonShape()
        shape.SetAsBox(boxWidth / 2, boxHeight / 2)

        fixture = b2FixtureDef()
        fixture.density = 1
        fixture.friction = 0.0
        fixture.shape = shape
        fixture.filter = b2Filter(
            groupIndex=0,
            categoryBits=0x0002,    # I am...
            maskBits=0x0001         # I collide with...
            )

        # body definition
        bodyDef = b2BodyDef()
        bodyDef.position.Set(boxPosition[0], boxPosition[1])
        bodyDef.type = b2_dynamicBody
        bodyDef.fixedRotation = False

        return self.m_simulation.addActor(ActorB2D(screenBoxPosition, (screenBoxWidth, screenBoxHeight)), bodyDef = bodyDef, fixture = fixture)

    def onKeyPress(self, event):
        if event == pygame.K_q:
            # apply gradual force upwards
            f = self.box.m_body.GetWorldVector(localVector=(0.0, 2000.0))
            p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 2.0))
            self.box.m_body.ApplyForce(f, p, True)
        #elif event == pygame.K_w:
        #    # apply immediate force upwards
        #    f = self.box.m_body.GetWorldVector(localVector=(0.0, 10.0))
        #    p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 2.0))
        #    self.box.m_body.ApplyLinearImpulse(f, p, True)
        elif event == pygame.K_LEFT:
            f = self.box.m_body.GetWorldVector(localVector=(-10.0, 0.0))
            p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 0.0))
            self.box.m_body.ApplyLinearImpulse(f, p, True)
        elif event == pygame.K_RIGHT:
            f = self.box.m_body.GetWorldVector(localVector=(10.0, 0.0))
            p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 0.0))
            self.box.m_body.ApplyLinearImpulse(f, p, True)

    def free(self):
        self.m_simulation.m_b2dWorld.DestroyJoint(self.j1)
        self.m_simulation.m_b2dWorld.DestroyJoint(self.j2)
        self.m_simulation.remove(j1)
        self.m_simulation.remove(j2)
        self.m_b2dWorld.DestroyBody(self.box)
        self.m_b2dWorld.DestroyBody(self.barA)
        self.m_b2dWorld.DestroyBody(self.barB)