import pygame
from screen_base import ScreenBase
from enums import ScreenType

class SimulationBase():
    def __init__(self, container, width, height):
        self.m_width = width
        self.m_height = height
        self.m_container = container
        print(self.m_container)

    def draw(self, screen):
        return pygame.sprite.LayeredDirty.draw(self.m_container, screen)
   
    def forceRedraw(self):
        pass

    def free(self):
        self.m_container = None