from b2d.actor_b2d import ActorB2D
from b2d.simulation_b2d import SimulationB2D
from Box2D import b2AABB, b2Vec2, b2QueryCallback, b2_dynamicBody, b2Color, b2CircleShape, b2FixtureDef, b2BodyDef, b2PolygonShape, b2Filter, b2_pi
import settings
import pygame
import neat
import pickle

class SimulationB2DTIP(SimulationB2D):
    def __init__(self, container, width, height, params):
        SimulationB2D.__init__(self, container, width, height)
        self.m_keyboardInputsEnabled = False
        self.m_isTraining = 'isTraining' in params and params['isTraining']
        self.m_trainingProgress = 0
        if 'genomes' in params and 'config' in params:
            self.initParams(params['genomes'], params['config'])
            self.m_trainingProgress = params['currentStep'] / settings.NEAT_TIP_EVOLVING_STEPS
        else:
            config = neat.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                'config_neat_tip')
            genome = pickle.load(open('winner_neat_tip.pkl', 'rb'))
            self.initParams([genome], config)

    def initParams(self, genomes, config):
        self.m_systems = [NNTIPSystem(self, genome, config) for genome in genomes]

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
            my_event = pygame.event.Event(settings.NEAT_TIP_EVENT_END_EVOLVING, message="Bad cat!")
            pygame.event.post(my_event)

        super().update(dt)

    def setupWorld(self):
        pass

    def init(self):
        actorGround = self.addActor(ActorB2D((400, 580), (800, 40)))
        actorGroundTop = self.addActor(ActorB2D((400, 520), (800, 40)))
        self.m_groundBody = actorGround.m_body

        actorGround.m_body.fixtures[0].filterData.maskBits=settings.B2D_CAT_BITS_CAR
        actorGround.m_body.fixtures[0].filterData.categoryBits=settings.B2D_CAT_BITS_GROUND
        actorGroundTop.m_body.fixtures[0].filterData.maskBits=settings.B2D_CAT_BITS_CAR
        actorGroundTop.m_body.fixtures[0].filterData.categoryBits=settings.B2D_CAT_BITS_GROUND

class NNTIPSystem(object):
    """ Description of the class """
    def __init__(self, simulation, genome, config):
        self.m_simulationRef = simulation

        self.m_isAlive = True

        # Added double inverted pendulum.
        self.m_dip = TIP(simulation)

        self.m_neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
        self.m_genome = genome

        self.m_timeAlive = 0
        self.m_traveledDistance = 0

    def update(self, dt):

        if not self.m_isAlive:
            return

        if self.m_simulationRef.m_isTraining:
            self.m_traveledDistance += abs(self.m_dip.box.m_speed[0]) * dt

            validAngle1 = -settings.NEAT_TIP_LIMIT_ANGLE < self.m_dip.barA.m_angle < settings.NEAT_TIP_LIMIT_ANGLE
            validAngle2 = -settings.NEAT_TIP_LIMIT_ANGLE < self.m_dip.barB.m_angle < settings.NEAT_TIP_LIMIT_ANGLE
            validAngle3 = -settings.NEAT_TIP_LIMIT_ANGLE < self.m_dip.barC.m_angle < settings.NEAT_TIP_LIMIT_ANGLE
            validPosition = 0 < self.m_dip.box.m_position.x < settings.APP_WIDTH
            validTime = self.m_timeAlive < settings.NEAT_TIP_MAX_TIME_ALIVE * 1000

            if not (validAngle1 and validAngle2 and validAngle3 and validPosition and validTime):
                if self.m_simulationRef.m_trainingProgress < 0.5:
                    self.m_genome.fitness = self.m_timeAlive
                else:
                    self.m_genome.fitness = max(0.0, self.m_timeAlive - self.m_traveledDistance/1000)
                #print('fitness: ' + str(self.m_genome.fitness) + "\t" + str(self.m_timeAlive) + "\t" + str(self.m_traveledDistance/1000))
                print('fitness: ' + str(self.m_genome.fitness))
                self.m_isAlive = False
                return

        inputAngle1 = ((self.m_dip.barA.m_angle + 180) % 360) - 180 # [-180,180]
        inputAngle2 = ((self.m_dip.barB.m_angle + 180) % 360) - 180 # [-180,180]
        inputAngle3 = ((self.m_dip.barB.m_angle + 180) % 360) - 180 # [-180,180]

        # Setup the input layer
        input = (inputAngle1,
                 self.m_dip.barA.m_rotSpeed,
                 inputAngle2,
                 self.m_dip.barB.m_rotSpeed,
                 inputAngle3,
                 self.m_dip.barC.m_rotSpeed,
                 settings.APP_WIDTH/2 - self.m_dip.box.m_position.x,
                 self.m_dip.box.m_speed[0])

        # Feed the neural network information
        output = self.m_neuralNetwork.activate(input)

        # Obtain Prediction
        f = self.m_dip.box.m_body.GetWorldVector(localVector=(min(max(-10,output[0]/10),10), 0.0))
        p = self.m_dip.box.m_body.GetWorldPoint(localPoint=(0.0, 0.0))
        self.m_dip.box.m_body.ApplyLinearImpulse(f, p, True)

        self.m_timeAlive += dt

    def free(self):
        self.m_dip.free()
        self.m_dip = None
        self.m_simulationRef = None

class TIP(object):
    def __init__(self, simulation):
        self.m_simulation = simulation
        self.box = self.m_simulation.createSimpleBox((400, 550), (40, 20), settings.B2D_CAT_BITS_CAR)
        self.barA = self.m_simulation.createSimpleBox((400, 490), (10, 100), settings.B2D_CAT_BITS_BAR)
        self.barB = self.m_simulation.createSimpleBox((400, 390), (10, 100), settings.B2D_CAT_BITS_BAR)
        self.barC = self.m_simulation.createSimpleBox((400, 290), (10, 100), settings.B2D_CAT_BITS_BAR)
        self.barC.m_body.angle = 1 * b2_pi/180

        self.j1 = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.box.m_body,
                                                       bodyB=self.barA.m_body,
                                                       localAnchorA=(0, 0),
                                                       localAnchorB=(0, -50/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=False,
                                                       lowerAngle=0,
                                                       upperAngle=0)
        self.j2 = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.barA.m_body,
                                                       bodyB=self.barB.m_body,
                                                       localAnchorA=(0, 50/settings.B2D_PPM),
                                                       localAnchorB=(0, -50/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=False,
                                                       lowerAngle=0,
                                                       upperAngle=0)
        self.j3 = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.barB.m_body,
                                                       bodyB=self.barC.m_body,
                                                       localAnchorA=(0, 50/settings.B2D_PPM),
                                                       localAnchorB=(0, -50/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=False,
                                                       lowerAngle=0,
                                                       upperAngle=0)
        simulation.m_joints.append(self.j1)
        simulation.m_joints.append(self.j2)
        simulation.m_joints.append(self.j3)

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
        self.m_simulation.m_b2dWorld.DestroyJoint(self.j3)
        self.m_simulation.m_joints.remove(self.j1)
        self.m_simulation.m_joints.remove(self.j2)
        self.m_simulation.m_joints.remove(self.j3)
        self.m_simulation.m_b2dWorld.DestroyBody(self.box.m_body)
        self.m_simulation.m_b2dWorld.DestroyBody(self.barA.m_body)
        self.m_simulation.m_b2dWorld.DestroyBody(self.barB.m_body)
        self.m_simulation.m_b2dWorld.DestroyBody(self.barC.m_body)
        self.m_simulation.removeActor(self.box)
        self.m_simulation.removeActor(self.barA)
        self.m_simulation.removeActor(self.barB)
        self.m_simulation.removeActor(self.barC)