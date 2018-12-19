import pygame
from screen_base import ScreenBase
from enums import ScreenType

class SimulationBase():
    def __init__(self, container, width, height):
        self.m_width = width
        self.m_height = height
        self.m_container = container
