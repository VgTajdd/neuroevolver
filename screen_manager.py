import pygame
from enums import ScreenType
import main_screen
import simulation_screen

class ScreenManager():
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.m_currentScreen = None
        self.m_currentScreenType = ScreenType.DEFAULT

    def draw(self, screen):
        pass

    def gotoScreen(self, type):
        if self.m_currentScreen != None:
            self.m_currentScreen.free()
        if type == ScreenType.MAIN_MENU:
            self.m_currentScreen = main_screen.MainMenu(0,0,(255,255,255))
        elif type == ScreenType.SIMULATION:
            self.m_currentScreen = simulation_screen.SimulationScreen(0,0,(255,255,255))
        self.m_currentScreenType = type

    def updateTime(self, dt):
        if self.m_currentScreen != None:
            self.m_currentScreen.updateTime(dt)

    def onKeyPress(self, key):
        if self.m_currentScreen != None:
            self.m_currentScreen.onMouseDown(key)

    def onMouseMove(self, event):
        if self.m_currentScreen != None:
            self.m_currentScreen.onMouseMove(event)

    def onMouseDown(self, event):
        if self.m_currentScreen != None:
            self.m_currentScreen.onMouseDown(event)

    def onMouseRelease(self, event):
        if self.m_currentScreen != None:
            self.m_currentScreen.onMouseMove(event)