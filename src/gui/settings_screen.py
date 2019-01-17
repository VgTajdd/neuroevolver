from core.screen_base import ScreenBase
from enums import ScreenType, SimulationType
import settings

class SettingsScreen(ScreenBase):
    def __init__(self, width, height, color):
        self.m_debugSimulation = None
        self.m_debugActors = None
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.SETTINGS

    def init(self):
        textDebugSim = 'SimulationDebugOff'
        if settings.SHOW_DEBUG_SHAPES: textDebugSim = 'SimulationDebugOn'
        textDebugAct = 'ActorsDebugOff'
        if settings.SHOW_ACTOR_RECT: textDebugAct = 'ActorsDebugOn'
        self.m_debugSimulation = self.addButton((400, 200), (200, 50), textDebugSim, self.toggleDebugSimulation)
        self.m_debugActors = self.addButton((400, 300), (200, 50), textDebugAct, self.toggleDebugActors)
        self.addButton((400, 400), (200, 50), 'Back', self.gotoMainMenu)
        self.addLabel((400, 100), (300, 50), 'Settings', alpha = 50)

    def toggleDebugSimulation(self):
        settings.SHOW_DEBUG_SHAPES = not settings.SHOW_DEBUG_SHAPES
        textDebugSim = 'SimulationDebugOff'
        if settings.SHOW_DEBUG_SHAPES: textDebugSim = 'SimulationDebugOn'
        self.m_debugSimulation.setText(textDebugSim)

    def toggleDebugActors(self):
        settings.SHOW_ACTOR_RECT = not settings.SHOW_ACTOR_RECT
        textDebugAct = 'ActorsDebugOff'
        if settings.SHOW_ACTOR_RECT: textDebugAct = 'ActorsDebugOn'
        self.m_debugActors.setText(textDebugAct)

    def gotoMainMenu(self):
        self.m_manager.gotoScreen(ScreenType.MAIN_MENU)