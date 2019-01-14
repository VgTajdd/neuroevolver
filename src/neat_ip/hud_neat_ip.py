from core.hud_base import HudBase
from enums import ScreenType

class HudNeatIP(HudBase):
    def __init__(self, width, height):
        HudBase.__init__(self, width, height)

    def init(self):
        self.showFPS()
        self.addLabel((75, 15), (150, 30), 'NEAT Inv-pendulum')
        #self.addButton((770, 15), (60, 30), 'Back', self.gotoMetamap, alpha = 200)
        #self.addImage((725, 550), (50, 50), "assets/imageqt.png")

    #def gotoMetamap(self):
    #    self.m_manager.gotoScreen(ScreenType.META_MAP)