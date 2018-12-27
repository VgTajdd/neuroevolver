import pygame
from screen_base import ScreenBase
import colors

class HudBase(ScreenBase):
    def __init__(self, width, height, color = colors.WHITE):
        ScreenBase.__init__(self, width, height, color)