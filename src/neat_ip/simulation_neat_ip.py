from core.simulation_base import SimulationBase
from physics.inverted_pendulum import InvertedPendulum
import neat
import pickle
import pygame
import settings
import math

class SimulationNeatIP(SimulationBase):
    def __init__(self, container, width, height, params):
        SimulationBase.__init__(self, container, width, height)
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
                'config')
            genome = pickle.load(open('winner.pkl', 'rb'))
            self.init([genome], config)

    def init(self, genomes, config):
        self.m_systems = [NNIPSystem(self, genome, config) for genome in genomes]

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
            my_event = pygame.event.Event(settings.EVENT_END_TRAINING_STEP, message="Bad cat!")
            pygame.event.post(my_event)

        super().update(dt)

class NNIPSystem(object):
    def __init__(self, simulation, genome, config):
        self.m_simulationRef = simulation

        self.m_isAlive = True

        # Added inverted pendulum.
        self.m_invertedPendulum = InvertedPendulum((settings.APP_WIDTH/2, 400), (10, 100), rc = (5, 100), layer = 2)
        self.m_invertedPendulum.addToSimulation(simulation)

        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome

        self.m_timeAlive = 0

    def update(self, dt):

        if not self.m_isAlive:
            return

        validAngle = -30 < self.m_invertedPendulum.m_angle < 30
        validPosition = 0 < self.m_invertedPendulum.m_position.x < settings.APP_WIDTH
        validTime = self.m_timeAlive < 5000

        if not (validAngle and validPosition and validTime) and self.m_simulationRef.m_isTraining:
            self.genome.fitness = self.m_timeAlive - 2 * math.fabs(settings.APP_WIDTH/2 - self.m_invertedPendulum.m_position.x)
            self.m_isAlive = False
            return

         # Setup the input layer
        input = (self.m_invertedPendulum.m_angle,
                 self.m_invertedPendulum.m_angularVelocity,
                 settings.APP_WIDTH/2 - self.m_invertedPendulum.m_position.x,
                 self.m_invertedPendulum.m_speedM)

        # Feed the neural network information
        output = self.neural_network.activate(input)

        # Obtain Prediction
        self.m_invertedPendulum.u = output[0]

        self.m_timeAlive += dt

    def free(self):
        self.m_invertedPendulum.removeFromSimulation(self.m_simulationRef)
        self.m_invertedPendulum = None
        self.m_simulationRef = None