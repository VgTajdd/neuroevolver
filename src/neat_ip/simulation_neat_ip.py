from core.simulation_base import SimulationBase
from physics.inverted_pendulum import InvertedPendulum
import neat
import pickle

class SimulationNeatIP(SimulationBase):
    def __init__(self, container, width, height, params):
        SimulationBase.__init__(self, container, width, height)
        if 'genomes' in params and 'config' in params:
            self.init(params['genomes'], params['config'])
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
        self.m_systems = [NNIPSystem(genome, config) for genome in genomes]

    def update(self, dt):
        # UPDATE INPUT HERE.
        super().update(dt)

class NNIPController(object):
    def __init__(self, ip):
        self.m_ip = ip

class NNIPSystem(object):
    def __init__(self, simulation, genome, config):
        self.m_simulationRef = simulation

        # Added inverted pendulum.
        self.m_invertedPendulum = InvertedPendulum((self.m_width/2, 400), (10, 100), rc = (5, 100), layer = 2)
        self.m_invertedPendulum.addToSimulation(self)
        self.m_controller = NNIPController(self.m_invertedPendulum)

        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
