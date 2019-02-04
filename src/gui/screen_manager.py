from enums import ScreenType, SimulationType
from gui.main_menu import MainMenu
from gui.metamap import Metamap
from gui.settings_screen import SettingsScreen
from core.simulation_screen import SimulationScreen
from steering.simulation_screen_steering import SimulationScreenSteering
from fpga.simulation_screen_fpga import SimulationScreenFPGA
from neat_ip.simulation_screen_neat_ip import SimulationScreenNeatIP
from neat_dycicle.simulation_screen_neat_dycicle import SimulationScreenNeatDycicle
from b2d.simulation_screen_b2d import SimulationScreenB2D
import core.colors as colors

class ScreenManager():
    def __init__(self, width, height):
        self.m_width = width
        self.m_height = height
        self.m_currentScreen = None
        self.m_currentScreenType = ScreenType.DEFAULT

    def draw(self, screen):
        return self.m_currentScreen.draw(screen)

    def gotoScreen(self, screenType, params = None):
        if self.m_currentScreen != None:
            self.m_currentScreen.free()
            self.m_currentScreen = None
        if screenType == ScreenType.MAIN_MENU:
            self.m_currentScreen = MainMenu(self.m_width, self.m_height, colors.BLACK)
        elif screenType == ScreenType.META_MAP:
            self.m_currentScreen = Metamap(self.m_width, self.m_height, colors.LIGHT_GRAY)
        elif screenType == ScreenType.SETTINGS:
            self.m_currentScreen = SettingsScreen(self.m_width, self.m_height, colors.GRAY)
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
                self.m_currentScreen = SimulationScreenFPGA(self.m_width, self.m_height, colors.GREY_BLUE)
            elif simulationType is SimulationType.NEAT_INVERTED_PENDULUM:
                self.m_currentScreen = SimulationScreenNeatIP(self.m_width, self.m_height, colors.WHITE, params)
            elif simulationType is SimulationType.NEAT_DYCICLE:
                self.m_currentScreen = SimulationScreenNeatDycicle(self.m_width, self.m_height, colors.GRAY, params)
            elif simulationType is SimulationType.B2D \
              or simulationType is SimulationType.NEAT_B2D_DIP \
              or simulationType is SimulationType.NEAT_B2D_WALKER:
                self.m_currentScreen = SimulationScreenB2D(self.m_width, self.m_height, colors.GRAY, params)
        else:
            self.m_currentScreen = SimulationScreen(self.m_width, self.m_height, colors.BEIGE)

    def updateTime(self, dt):
        if self.m_currentScreen != None:
            self.m_currentScreen.updateTime(dt)

    def onKeyPress(self, key):
        if self.m_currentScreen != None:
            self.m_currentScreen.onKeyPress(key)

    def onKeyRelease(self, key):
        if self.m_currentScreen != None:
            self.m_currentScreen.onKeyRelease(key)

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