import pygame
from enums import ScreenType
import main_menu
import simulation_screen
import colors

class ScreenManager():
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.m_currentScreen = None
        self.m_currentScreenType = ScreenType.DEFAULT

    def draw(self, screen):
        return self.m_currentScreen.draw(screen);

    def gotoScreen(self, typeScreen):
        if self.m_currentScreen != None:
            self.m_currentScreen.free()
        if typeScreen == ScreenType.MAIN_MENU:
            self.m_currentScreen = main_menu.MainMenu(0,0,colors.PEACH)
        elif typeScreen == ScreenType.SIMULATION:
            self.m_currentScreen = simulation_screen.SimulationScreen(0,0,colors.PINK)
        self.m_currentScreenType = typeScreen
        self.m_currentScreen.setManager(self)

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
            self.m_currentScreen.onMouseRelease(event)

    def forceRedraw(self):
        if self.m_currentScreen:
            self.m_currentScreen.forceRedraw()