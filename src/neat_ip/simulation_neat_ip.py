## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## simulation_neat_ip.py                                                     ##
## ========================================================================= ##

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
                '../config_files/config_neat_ip')
            genome = pickle.load(open('../pkl_files/winner_neat_ip.pkl', 'rb'))
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
            my_event = pygame.event.Event(settings.NEAT_IP_EVENT_END_EVOLVING, message="Bad cat!")
            pygame.event.post(my_event)

        super().update(dt)

class NNIPSystem(object):
    def __init__(self, simulation, genome, config):
        self.m_simulationRef = simulation

        self.m_isAlive = True

        # Added inverted pendulum.
        self.m_invertedPendulum = InvertedPendulum((settings.APP_WIDTH/2, 400), (10, 100), rc = (5, 100), layer = 2)
        self.m_invertedPendulum.addToSimulation(simulation)
        self.m_invertedPendulum.m_angle = settings.NEAT_IP_INITIAL_ANGLE

        self.m_neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
        self.m_genome = genome

        self.m_timeAlive = 0
        self.m_traveledDistance = 0

    def update(self, dt):
        if not self.m_isAlive:
            return

        if self.m_simulationRef.m_isTraining:
            self.m_traveledDistance += abs(self.m_invertedPendulum.m_speedM) * dt

            validAngle = -settings.NEAT_IP_LIMIT_ANGLE < self.m_invertedPendulum.m_angle < settings.NEAT_IP_LIMIT_ANGLE
            validPosition = 0 < self.m_invertedPendulum.m_position.x < settings.APP_WIDTH
            validTime = self.m_timeAlive < settings.NEAT_IP_MAX_TIME_ALIVE * 1000

            if not (validAngle and validPosition and validTime):
                deltaX = abs(settings.APP_WIDTH/2 - self.m_invertedPendulum.m_position.x)
                print('fitness: ' + str(self.m_timeAlive) + ' ' + str(-self.m_traveledDistance/5) + ' ' + str(-deltaX*5) + ' ' + str(self.m_timeAlive - self.m_traveledDistance/5 - deltaX*5))
                self.m_genome.fitness = max(0,self.m_timeAlive - self.m_traveledDistance/5 - deltaX*5)
                self.m_isAlive = False
                return

        inputAngle = ((self.m_invertedPendulum.m_angle + 180) % 360) - 180 # [-180,180]

         # Setup the input layer
        input = (inputAngle,
                 self.m_invertedPendulum.m_angularVelocity,
                 settings.APP_WIDTH/2 - self.m_invertedPendulum.m_position.x,
                 self.m_invertedPendulum.m_speedM)

        # Feed the neural network information
        output = self.m_neuralNetwork.activate(input)

        # Obtain Prediction
        self.m_invertedPendulum.u = output[0]

        self.m_timeAlive += dt

    def free(self):
        self.m_invertedPendulum.removeFromSimulation(self.m_simulationRef)
        self.m_invertedPendulum = None
        self.m_simulationRef = None