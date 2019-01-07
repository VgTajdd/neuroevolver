from core.screen_base import ScreenBase
from enums import ScreenType
from enums import SimulationType

class Metamap(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP

    def init(self):
        self.addButton((400, 200), (200, 50), 'Simple Steering', self.gotoSimpleSteering)
        self.addButton((400, 300), (200, 50), 'Food Poison GA', self.gotoFPSteering)
        self.addButton((400, 400), (200, 50), 'Back', self.gotoMainMenu)
        self.addLabel((400, 100), (300, 50), 'Choose Simulation', alpha = 50)

    def gotoSimpleSteering(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.SIMPLE_STEERING})

    def gotoFPSteering(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.FP_STEERING})

    def gotoMainMenu(self):
        self.m_manager.gotoScreen(ScreenType.MAIN_MENU)