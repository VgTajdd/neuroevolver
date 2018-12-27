import pygame
from constants.enums import ScreenType
from main_menu import MainMenu
from simulation_screen_steering import SimulationScreenSteering
import constants.colors as colors

class ScreenManager():
    def __init__(self, width, height):
        self.m_width = width
        self.m_height = height
        self.m_currentScreen = None
        self.m_currentScreenType = ScreenType.DEFAULT

    def draw(self, screen):
        return self.m_currentScreen.draw(screen);

    def gotoScreen(self, typeScreen):
        if self.m_currentScreen != None:
            self.m_currentScreen.free()
        if typeScreen == ScreenType.MAIN_MENU:
            self.m_currentScreen = MainMenu(self.m_width, self.m_height, colors.PEACH)
        elif typeScreen == ScreenType.SIMULATION:
            self.m_currentScreen = SimulationScreenSteering(self.m_width, self.m_height, colors.BEIGE)
        self.m_currentScreenType = typeScreen
        self.m_currentScreen.setManager(self)

    def updateTime(self, dt):
        if self.m_currentScreen != None:
            self.m_currentScreen.updateTime(dt)

    def onKeyPress(self, key):
        if self.m_currentScreen != None:
            self.m_currentScreen.onKeyPress(key)

    def onMouseMove(self, event):
        if self.m_currentScreen != None:
            self.m_currentScreen.onMouseMove(event)

    def onMouseDown(self, event):
        if self.m_currentScreen != None:
            self.m_currentScreen.onMouseDown(event)

    def onMouseRelease(self, event):
        if self.m_currentScreen != None:
            self.m_currentScreen.onMouseRelease(event)

    def forceRedraw(self):
        if self.m_currentScreen != None:
            self.m_currentScreen.forceRedraw()