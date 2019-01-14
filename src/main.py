from core.application import Application
import argparse
import neat

def main():
    app = Application()

    parser = argparse.ArgumentParser(description='Run the program')
    parser.add_argument("--trainMode", help="Mode of training")

    args = parser.parse_args()

    if args.trainMode and args.trainMode.upper() == "NEATIP":
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            'config')
        app.trainNeatIP([], config)
    else:
        app.play()

if __name__ == "__main__":
    main()
