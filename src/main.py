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

def trainMode(fileNameConfig, steps_number, eval_genomes):
    config = createNeatConfig(fileNameConfig)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, n = steps_number)
    filename = savePickle(winner, 'winner_neat.pkl')
    path = getPathWithoutExtension(filename)
    neat_utils.visualize.draw_net(config, winner, False, filename=path, fmt="png")
    neat_utils.visualize.plot_stats(stats, ylog=False, view=False, filename=path+".svg")

def train(mode):

    global trainingCurrentStep
    trainingCurrentStep = 0

    if mode.upper() == "NEAT_IP":
        trainMode('config_neat_ip', settings.NEAT_IP_TRAINING_STEPS, eval_genomes_neat_ip)
    elif mode.upper() == "NEAT_DYCICLE":
        trainMode('config_neat_dycicle', settings.NEAT_DYCICLE_TRAINING_STEPS, eval_genomes_neat_dycicle)
    elif mode.upper() == "NEAT_DIP":
        trainMode('config_neat_dip', settings.NEAT_DIP_TRAINING_STEPS, eval_genomes_neat_dip)
    elif mode.upper() == "NEAT_TIP":
        trainMode('config_neat_tip', settings.NEAT_TIP_TRAINING_STEPS, eval_genomes_neat_tip)
    elif mode.upper() == "NEAT_WALKER":
        trainMode('config_neat_walker', settings.NEAT_WALKER_TRAINING_STEPS, eval_genomes_neat_walker)
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
