from core.hud_base import HudBase
from enums import ScreenType

class HudFPGA(HudBase):
    def __init__(self, width, height):
        HudBase.__init__(self, width, height)

    def init(self):
        self.showFPS()
        self.addLabel((80, 30), (150, 30), 'Food Poison GA')
        self.addButton((725, 40), (100, 50), 'Back', self.gotoMetamap)
        #self.addImage((725, 550), (50, 50), "assets/imageqt.png")

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)