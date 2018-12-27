import pygame
from core.screen_base import ScreenBase
import core.colors as colors

class HudBase(ScreenBase):
    def __init__(self, width, height, color = colors.WHITE):
        ScreenBase.__init__(self, width, height, color)