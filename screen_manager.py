from enum import IntEnum
import pygame
import main_screen
import simulation_screen

class ScreenType(IntEnum):
    DEFAULT = 0
    MAIN_MENU = 1
    SIMULATION = 2

class ScreenManager():
    def __init__(self, width, height):

        self.w = width
        self.h = height
        self.m_currentScreen = None
        self.m_currentScreenType = ScreenType.DEFAULT;

    def draw(self, screen):
        pass

    def gotoScreen(self, type):
        if ( self.m_currentScreen != None ):
            self.m_currentScreen.free()
        if type == ScreenType.GUI_MAIN_MENU:
            self.m_currentScreen = main_screen.MainMenu(self)
        elif type == ScreenType.GUI_SIMULATION:
            self.m_currentScreen = simulation_screen.SimulationScreen(self)
        self.m_currentScreenType = type

    def updateTime(self, dt):
        if ( self.m_currentScreen != None ):
            self.m_currentScreen.updateTime(dt)

    def onKeyPress(self, key):
        if ( self.m_currentScreen != None ):
            self.m_currentScreen.onMouseDown(key)

    def onMouseMove(self, event):
        if ( self.m_currentScreen != None ):
            self.m_currentScreen.onMouseMove(event)

    def onMouseDown(self, event):
        if ( self.m_currentScreen != None ):
            self.m_currentScreen.onMouseDown(event)

    def onMouseRelease(self, event):
        if ( self.m_currentScreen != None ):
            self.m_currentScreen.onMouseMove(event)