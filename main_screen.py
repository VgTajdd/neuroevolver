import pygame
from screen_base import ScreenBase 
from screen_manager import ScreenType
import screen_manager

class MainMenu(ScreenBase):
    def __init__(self, width, height, color):
        SreenBase.__init__(self)

    self.m_type = screen_manager.ScreenType.MAIN_MENU