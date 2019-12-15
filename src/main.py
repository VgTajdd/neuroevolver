from core.application import Application
import argparse
import neat
import pickle
import settings
import neat_utils.visualize
from core.utils import savePickle, getPathWithoutExtension

trainingCurrentStep = 0

def main():

    parser = argparse.ArgumentParser(description='Run the program')
    parser.add_argument("--trainMode", help="Mode of training")

    args = parser.parse_args()

    settings.TRAIN_CALLBACK = train

    if args.trainMode:
        train(args.trainMode)
    else:
        app = Application()
        app.play()

def trainMode(fileNameConfig, steps_number, eval_genomes, node_names=None):
    config = createNeatConfig(fileNameConfig)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, n = steps_number)
    filename = savePickle(winner, '../pkl_files/winner_neat.pkl')
    path = getPathWithoutExtension(filename)
    neat_utils.visualize.draw_net(config, winner, False, filename=path, fmt="png", node_names=node_names)
    neat_utils.visualize.plot_stats(stats, ylog=False, view=False, filename=path+".svg")

def train(mode):

    global trainingCurrentStep
    trainingCurrentStep = 0

    if mode == settings.NEAT_IP_KEY:
        trainMode('../config_files/config_neat_ip', settings.NEAT_IP_EVOLVING_STEPS, eval_genomes_neat_ip)
    elif mode == settings.NEAT_DYCICLE_KEY:
        trainMode('../config_files/config_neat_dycicle', settings.NEAT_DYCICLE_EVOLVING_STEPS, eval_genomes_neat_dycicle)
    elif mode == settings.NEAT_DIP_KEY:
        node_names = {-1:'a1', -2: 'a*1',-3:'a2', -4: 'a*2',-5:'a0', -6: 'a*0', 0:'u'}
        trainMode('../config_files/config_neat_dip', settings.NEAT_DIP_EVOLVING_STEPS, eval_genomes_neat_dip, node_names)
    elif mode == settings.NEAT_TIP_KEY:
        trainMode('../config_files/config_neat_tip', settings.NEAT_TIP_EVOLVING_STEPS, eval_genomes_neat_tip)
    elif mode == settings.NEAT_WALKER_KEY:
        trainMode('../config_files/config_neat_walker', settings.NEAT_WALKER_EVOLVING_STEPS, eval_genomes_neat_walker)
    app = Application()
    app.play()

def createNeatConfig(filename):
    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultStagnation,
                         filename)
    return config

def eval_genomes_neat_ip(genomes, config):
    idx, genomes = zip(*genomes)
    app = Application()
    global trainingCurrentStep
    trainingCurrentStep += 1
    app.trainNeatIP(genomes, config, trainingCurrentStep)

def eval_genomes_neat_dip(genomes, config):
    idx, genomes = zip(*genomes)
    app = Application()
    global trainingCurrentStep
    trainingCurrentStep += 1
    app.trainNeatDIP(genomes, config, trainingCurrentStep)

def eval_genomes_neat_tip(genomes, config):
    idx, genomes = zip(*genomes)
    app = Application()
    global trainingCurrentStep
    trainingCurrentStep += 1
    app.trainNeatTIP(genomes, config, trainingCurrentStep)

def eval_genomes_neat_dycicle(genomes, config):
    idx, genomes = zip(*genomes)
    app = Application()
    global trainingCurrentStep
    trainingCurrentStep += 1
    app.trainNeatDycicle(genomes, config, trainingCurrentStep)

def eval_genomes_neat_walker(genomes, config):
    idx, genomes = zip(*genomes)
    app = Application()
    global trainingCurrentStep
    trainingCurrentStep += 1
    app.trainNeatWalker(genomes, config, trainingCurrentStep)
    #neat_utils.visualize.draw_net(config, genomes[0], False, filename="net_neat_walker", fmt="png")

if __name__ == "__main__":
    main()
