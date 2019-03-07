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
        return pickle.load(open(filename, 'rb'))
    return None

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