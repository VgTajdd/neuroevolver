import pygame
import pickle
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

def existsFile(path):
    my_file = Path(path)
    if my_file.is_file():
        # file exists
        return True
    return False

def existsDir(path):
    my_file = Path(path)
    if my_file.is_dir():
        # dir exists
        return True
    return False

def getPathWithoutExtension(path):
    my_file = Path(path)
    res = path
    if my_file.is_file():
        suffix = my_file.suffix
        res = str(path).replace(suffix,'')
    return res

def getImageSize(path):
    image = pygame.image.load(path)
    rect = image.get_rect()
    return (rect[2], rect[3])

def loadPickle(defaultPath):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(filetypes=[("Pkl files", "*.pkl")]) # show an "Open" dialog box and return the path to the selected file
    if len(filename) == 0:
        filename = defaultPath
    if filename:
        return filename, pickle.load(open(filename, 'rb'))
    return filename, None

def savePickle(obj, defaultPath):
    Tk().withdraw()
    filename = asksaveasfilename(filetypes=[("Pkl files", "*.pkl")])
    file_path = Path(filename)
    file_path = file_path.with_suffix('.pkl')
    filename = file_path.as_posix()
    if len(filename) == 0:
        filename = defaultPath
    if filename:
        pickle.dump(obj, open(filename, 'wb'))
    return filename

import neat
import neat_utils.visualize

# Use this way:
# generatePickleGraph(defaultPath='../pkl_files/winner_neat_dip.pkl', configFile='../config_files/config_neat_dip')
def generatePickleGraph(defaultPath, configFile):
    pickleBundle = loadPickle(defaultPath=defaultPaht)
    config = neat.Config(neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        '../config_files/config_neat_dip')
    path = getPathWithoutExtension(pickleBundle[0])
    node_names = {-1:'a1', -2: 'a1\'',-3:'a2', -4: 'a2\'',-5:'a0', -6: 'a0\'', 0:'u'}
    neat_utils.visualize.draw_net(config, pickleBundle[1], False, filename=path, fmt="png", node_names=node_names)