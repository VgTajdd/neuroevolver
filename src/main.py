from core.application import Application
import argparse
import neat
import pickle
import settings
import neat_utils.visualize

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

def train(mode):

    global trainingCurrentStep
    trainingCurrentStep = 0

    if mode.upper() == "NEAT_IP":
        config = createNeatConfig('config_neat_ip')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        winner = p.run(eval_genomes_neat_ip, n = settings.NEAT_IP_TRAINING_STEPS)
        pickle.dump(winner, open('winner_neat_ip.pkl', 'wb'))
        neat_utils.visualize.draw_net(config, winner, False, filename="net_neat_ip", fmt="png")

    elif mode.upper() == "NEAT_DYCICLE":
        config = createNeatConfig('config_neat_dycicle')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        winner = p.run(eval_genomes_neat_dycicle, n = settings.NEAT_DYCICLE_TRAINING_STEPS)
        pickle.dump(winner, open('winner_neat_dycicle.pkl', 'wb'))
        neat_utils.visualize.draw_net(config, winner, False, filename="net_neat_dycicle", fmt="png")

    elif mode.upper() == "NEAT_DIP":
        config = createNeatConfig('config_neat_dip')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        winner = p.run(eval_genomes_neat_dip, n = settings.NEAT_DIP_TRAINING_STEPS)
        pickle.dump(winner, open('winner_neat_dip.pkl', 'wb'))
        neat_utils.visualize.draw_net(config, winner, False, filename="net_neat_dip", fmt="png")

    elif mode.upper() == "NEAT_TIP":
        config = createNeatConfig('config_neat_tip')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        winner = p.run(eval_genomes_neat_tip, n = settings.NEAT_TIP_TRAINING_STEPS)
        pickle.dump(winner, open('winner_neat_tip.pkl', 'wb'))
        neat_utils.visualize.draw_net(config, winner, False, filename="net_neat_tip", fmt="png")

    elif mode.upper() == "NEAT_WALKER":
        config = createNeatConfig('config_neat_walker')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        winner = p.run(eval_genomes_neat_walker, n = settings.NEAT_WALKER_TRAINING_STEPS)
        pickle.dump(winner, open('winner_neat_walker.pkl', 'wb'))
        neat_utils.visualize.draw_net(config, winner, False, filename="net_neat_walker", fmt="png")

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
