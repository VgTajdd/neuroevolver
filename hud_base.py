import pygame
from screen_base import ScreenBase
from enums import ScreenType
from control import Label
from control import Button
import colors

class HudBase(ScreenBase):
    def __init__(self, width, height, color = colors.WHITE):
        ScreenBase.__init__(self, width, height, color)

    def init(self):
        btn = Button((725,50), (100, 50), layer = 100)
        btn.setText('Return')
        btn.setCallback(self.gotoMainMenu)
        label = Label((75,50), (100, 50), 'Hud', layer = 100)
        self.addControl(label)
        self.addControl(btn)

    def gotoMainMenu(self):
        self.m_manager.gotoScreen(ScreenType.MAIN_MENU)
