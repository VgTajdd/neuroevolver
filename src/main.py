from core.application import Application
import argparse
import neat
import pickle
import settings

trainingCurrentStep = 0

def main():

    parser = argparse.ArgumentParser(description='Run the program')
    parser.add_argument("--trainMode", help="Mode of training")

    args = parser.parse_args()

    global trainingCurrentStep

    #if args.trainMode and args.trainMode.upper() == "NEATIP":
    #    trainingCurrentStep = 0

    #    config = neat.Config(
    #        neat.DefaultGenome,
    #        neat.DefaultReproduction,
    #        neat.DefaultSpeciesSet,
    #        neat.DefaultStagnation,
    #        'config_neat_ip')
    #    p = neat.Population(config)
    #    p.add_reporter(neat.StdOutReporter(True))
    #    winner = p.run(eval_genomes_neat_ip, n = settings.NEATIP_TRAINING_STEPS)
    #    pickle.dump(winner, open('winner_neat_ip.pkl', 'wb'))

    #elif args.trainMode and args.trainMode.upper() == "NEAT_DYCICLE":
    #    trainingCurrentStep = 0

    #    config = neat.Config(
    #        neat.DefaultGenome,
    #        neat.DefaultReproduction,
    #        neat.DefaultSpeciesSet,
    #        neat.DefaultStagnation,
    #        'config_neat_dycicle')
    #    p = neat.Population(config)
    #    p.add_reporter(neat.StdOutReporter(True))
    #    winner = p.run(eval_genomes_neat_dycicle, n = settings.NEAT_DYCICLE_TRAINING_STEPS)
    #    pickle.dump(winner, open('winner_neat_dycicle.pkl', 'wb'))

    #elif args.trainMode and args.trainMode.upper() == "NEATDIP":
    #    trainingCurrentStep = 0

    #    config = neat.Config(
    #        neat.DefaultGenome,
    #        neat.DefaultReproduction,
    #        neat.DefaultSpeciesSet,
    #        neat.DefaultStagnation,
    #        'config_neat_dip')
    #    p = neat.Population(config)
    #    p.add_reporter(neat.StdOutReporter(True))
    #    winner = p.run(eval_genomes_neat_dip, n = settings.NEAT_DIP_TRAINING_STEPS)
    #    pickle.dump(winner, open('winner_neat_dip.pkl', 'wb'))

    #elif args.trainMode and args.trainMode.upper() == "NEAT_WALKER":
    if True:
        trainingCurrentStep = 0

        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            'config_neat_walker')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        winner = p.run(eval_genomes_neat_walker, n = settings.NEAT_WALKER_TRAINING_STEPS)
        pickle.dump(winner, open('winner_neat_walker.pkl', 'wb'))

    app = Application()
    app.play()

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

if __name__ == "__main__":
    main()
