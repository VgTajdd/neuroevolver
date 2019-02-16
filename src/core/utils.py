import pygame
from pathlib import Path

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

def getImageSize(path):
    image = pygame.image.load(path)
    rect = image.get_rect()
    return (rect[2], rect[3])
