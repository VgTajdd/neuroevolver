from core.simulation_base import SimulationBase
from core.debug_drawing import DebugDrawing
from neat_dycicle.dycicle import Dycicle
from pygame.math import Vector2
import core.colors as colors
import neat
import pickle
import pygame
import settings
import math
import random

class SimulationNeatDycicle(SimulationBase):
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
                '../config_files/config_neat_dycicle')
            genome = pickle.load(open('../pkl_files/winner_neat_dycicle.pkl', 'rb'))
            self.init([genome], config)

    def init(self, genomes, config):
        self.m_systems = [NNDycicleSystem(self, genome, config) for genome in genomes]
        self.m_world = NeatDycicleWorld()

    def update(self, dt):
        self.m_world.m_debugShapes.clear()

        if len(self.m_systems) == 0:
            return

        for system in self.m_systems:
            if not system.m_isAlive:
                self.m_systems.remove(system)
                system.free()
                continue
            system.update(dt)

        if len(self.m_systems) == 0:
            my_event = pygame.event.Event(settings.NEAT_DYCICLE_EVENT_END_EVOLVING, message="Bad cat!")
            pygame.event.post(my_event)

        super().update(dt)
        for system in self.m_systems:
            self.m_debugContainer += system.m_dycicle.m_debugShapes
        self.m_world.addWallShapes()
        self.m_debugContainer += self.m_world.m_debugShapes

class NNDycicleSystem(object):
    def __init__(self, simulation, genome, config):
        self.m_simulationRef = simulation

        self.m_isAlive = True

        # Added dycicle.
        randomX = random.randint(120, 130)
        randomY = random.randint(200, 400)
        self.m_dycicle = Dycicle((randomX, randomY), (20, 20), imagePath = "assets/actor0.png", layer = 2)
        simulation.addActor(self.m_dycicle)

        self.m_dycicle.radius = 10

        self.m_neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
        self.m_genome = genome

        self.m_timeAlive = 0
        self.m_traveledDistance = 0
        self.m_start = self.m_dycicle.m_position

    def update(self, dt):

        if not self.m_isAlive:
            return

        if self.m_simulationRef.m_isTraining:
            self.m_traveledDistance += abs(self.m_dycicle.m_speedL + self.m_dycicle.m_speedR) * dt / 2000

            invalidTime = self.m_timeAlive >= settings.NEAT_DYCICLE_MAX_TIME_ALIVE * 1000
            existsCollision = self.m_simulationRef.m_world.collidesWithWall(self.m_dycicle)

            if invalidTime or existsCollision:
                spinCount = int(abs(self.m_dycicle.m_angle) / 360)
                self.m_genome.fitness = self.m_traveledDistance
                if spinCount > 0:
                    self.m_genome.fitness = self.m_traveledDistance/(spinCount*3)
                print('fitness: ' + str(self.m_genome.fitness) + '  ' + str(spinCount))
                self.m_isAlive = False
                return

        # Setup the input layer
        input = self.m_simulationRef.m_world.checkAntennaCollision(self.m_dycicle)

        # Feed the neural network information
        output = self.m_neuralNetwork.activate(input)

        # Obtain Prediction
        self.m_dycicle.m_speedL = 150 * output[0]
        self.m_dycicle.m_speedR = 150 * output[1]

        self.m_timeAlive += dt

    def free(self):
        self.m_simulationRef.removeActor(self.m_dycicle)
        self.m_dycicle.free()
        self.m_dycicle = None
        self.m_simulationRef = None

class NeatDycicleWorld(object):
    def __init__(self):
        self.m_walls = []
        outter = [(100,100), (700,100), (700,500), (100,500), (100,100)]
        inner = [(150,150), (650,150), (650,450), (150,450), (150,150)]
        self.m_walls = [Wall(outter[i], outter[i+1], self) for i in range(4)]
        self.m_walls += [Wall(inner[i], inner[i+1], self) for i in range(4)]
        self.m_debugShapes = []

    def addWallShapes(self):
        self.m_debugShapes.append(DebugDrawing.rect(colors.BLUE, [100, 100, 600, 400]))
        self.m_debugShapes.append(DebugDrawing.rect(colors.BLUE, [150, 150, 500, 300]))

    def checkAntennaCollision(self, dycicle):
        colls = [1 for i in range(5)]
        for wall in self.m_walls:
            c = wall.checkAntennaCollision(dycicle)
            for i in range(5):
                colls[i] = min(c[i], colls[i])
        return colls

    def collidesWithWall(self, dycicle):
        for wall in self.m_walls:
            if wall.collideWith(dycicle):
                return True
        return False

class Wall(object):
    def __init__(self, _p1, _p2, world):
        self.p1 = _p1
        self.p2 = _p2
        self.m_world = world

    def checkAntennaCollision(self, dycicle):
        colls = []
        for antenna in dycicle.m_antennas:
            line_antenna = dycicle.m_position, dycicle.m_position + antenna
            intersection = self.getIntersection((self.p1, self.p2), line_antenna)
            if intersection:
                self.m_world.m_debugShapes.append(DebugDrawing.ellipse(colors.RED, [intersection[0]-2,intersection[1]-2, 4, 4], 2))
                v = Vector2(intersection) - dycicle.m_position
                factor = v.length()/dycicle.m_antennaLength
                colls.append(factor)
            else:
                colls.append(1)
        return colls

    def getIntersection(self, segment1, segment2):
        A=segment1[0]
        B=segment1[1]
        C=segment2[0]
        D=segment2[1]
        u=Vector2(B)-A
        v=Vector2(D)-C
        if u.length() == 0 or v.length() == 0:
            return None
        if (u.y*v.x-u.x*v.y) == 0:
            return None
        r = (A[0]*u.y-A[1]*u.x-C[0]*u.y+C[1]*u.x)/(u.y*v.x-u.x*v.y)
        t = 0
        if u.x != 0:
            t = (r*v.x+C[0]-A[0])/(u.x)
        else:
            t = (r*v.y+C[1]-A[1])/(u.y)
        if 0<=t<=1 and 0<=r<=1:
            return A + t*u
        return None

    def collideWith(self, actor): # segment-circle intersection
        u = Vector2(self.p2)-self.p1
        j=self.p1[0]-actor.m_position.x
        k=self.p1[1]-actor.m_position.y
        a=u.length()
        a=a*a
        b=2*j*u.x + 2*k*u.y
        c=j*j+k*k-actor.radius*actor.radius
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return False
        t1 = (-b-pow(discriminant, 0.5))/(2*a)
        t2 = (-b+pow(discriminant, 0.5))/(2*a)
        if 0<=t1<=1:
            return True
        if 0<=t2<=1:
            return True
        return False