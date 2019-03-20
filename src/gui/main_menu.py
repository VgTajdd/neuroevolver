from core.screen_base import ScreenBase
import core.colors as colors
from enums import ScreenType
from enums import SimulationType

class MainMenu(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.MAIN_MENU

    def init(self):
        #demoButton = Button((400,300), (100, 50))
        #demoButton.setText('DemoButton')
        #demoButton.resize(200, 50)
        #demoButton.setPosition(650, 550)
        #demoButton.setCallback(self.gotoSimulation)
        #self.addControl(demoButton)
        self.addButton((650, 550), (200, 50), 'Selector', self.gotoMetamap, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((150, 550), (200, 50), 'Settings', self.gotoSettings, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addLabel((400,300), (400, 100), "Genetic Algorithms and Neuroevolution", alpha = 255)

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)

    def gotoSettings(self):
        self.m_manager.gotoScreen(ScreenType.SETTINGS)