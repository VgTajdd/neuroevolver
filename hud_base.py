import pygame
from screen_base import ScreenBase
from enums import ScreenType
import colors

class HudBase(ScreenBase):
    def __init__(self, width, height, color = colors.WHITE):
        ScreenBase.__init__(self, width, height, color)
        #self.m_type = ScreenType.SIMULATION