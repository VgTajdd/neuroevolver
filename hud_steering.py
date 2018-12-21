import pygame
from hud_base import HudBase
from enums import ScreenType

class HudSteering(HudBase):
    def __init__(self, width, height):
        HudBase.__init__(self, width, height)

    def init(self):
        self.addLabel((50,25), (80, 30), 'HudText', layer = 100)
        self.addButton((725,50), (100, 50), 'BackButton', self.gotoMainMenu, layer = 100)
        self.addImage((725,550), (50, 50), "assets/imageqt.png", layer = 100)

    def gotoMainMenu(self):
        self.m_manager.gotoScreen(ScreenType.MAIN_MENU)
