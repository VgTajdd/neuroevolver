import pygame
from hud_base import HudBase
from enums import ScreenType

class Hud(HudBase):
    def __init__(self, width, height):
        HudBase.__init__(self, width, height)

    def init(self):
        self.addLabel((75,50), (100, 50), 'HudText')
        self.addButton((725,50), (100, 50), 'BackButton', self.gotoMainMenu)
        self.addImage((400,300), (100, 100), "assets/imageqt.png")

    def gotoMainMenu(self):
        self.m_manager.gotoScreen(ScreenType.MAIN_MENU)
