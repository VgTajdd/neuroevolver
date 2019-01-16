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

    if args.trainMode and args.trainMode.upper() == "NEATIP":
    #if True:
        global trainingCurrentStep
        trainingCurrentStep = 0

        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            'config')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        winner = p.run(eval_genomes, n = settings.NEATIP_TRAINING_STEPS)
        pickle.dump(winner, open('winner.pkl', 'wb'))
    #else:
    app = Application()
    app.play()

def eval_genomes(genomes, config):
    idx, genomes = zip(*genomes)
    app = Application()
    global trainingCurrentStep
    trainingCurrentStep += 1
    app.trainNeatIP(genomes, config, trainingCurrentStep)

if __name__ == "__main__":
    main()
