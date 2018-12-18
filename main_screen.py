import pygame
from screen_base import ScreenBase
from enums import ScreenType
from control import Button

class MainMenu(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.MAIN_MENU

    def init(self):
        demoButton = Button((400,300), (100, 50))
        demoButton.setText('DemoButton')
        demoButton.resize(200, 50)
        demoButton.setPosition(100, 25)
        self.addControl(demoButton)