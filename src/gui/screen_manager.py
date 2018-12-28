import pygame
from enums import ScreenType
from enums import SimulationType
from gui.main_menu import MainMenu
from core.simulation_screen import SimulationScreen
from steering.simulation_screen_steering import SimulationScreenSteering
import core.colors as colors

class ScreenManager():
    def __init__(self, width, height):
        self.m_width = width
        self.m_height = height
        self.m_currentScreen = None
        self.m_currentScreenType = ScreenType.DEFAULT

    def draw(self, screen):
        return self.m_currentScreen.draw(screen);

    def gotoScreen(self, screenType, params = None):
        if self.m_currentScreen != None:
            self.m_currentScreen.free()
            self.m_currentScreen = None
        if screenType == ScreenType.MAIN_MENU:
            self.m_currentScreen = MainMenu(self.m_width, self.m_height, colors.PEACH)
        elif screenType == ScreenType.SIMULATION:
            self.createSimulationScreen(params)
        else: return
        self.m_currentScreenType = screenType
        self.m_currentScreen.setManager(self)

    def createSimulationScreen(self, params):
        if params and params['simulationType']:
            simulationType = params['simulationType']
            if simulationType is SimulationType.SIMPLE_STEERING:
                self.m_currentScreen = SimulationScreenSteering(self.m_width, self.m_height, colors.BEIGE)
            elif simulationType is SimulationType.FP_STEERING:
                self.m_currentScreen = SimulationScreenSteering(self.m_width, self.m_height, colors.BEIGE)
        else:
            self.m_currentScreen = SimulationScreen(self.m_width, self.m_height, colors.BEIGE)

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