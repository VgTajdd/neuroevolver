from core.screen_base import ScreenBase
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
        self.addButton((650, 550), (200, 50), 'DemoButton', self.gotoMetamap)
        self.addLabel((400,300), (100, 50), 'MainMenu', alpha = 128)

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)