from core.hud_base import HudBase
from enums import ScreenType

class HudFPGA(HudBase):
    def __init__(self, width, height):
        self.m_fpsLabel = None
        HudBase.__init__(self, width, height)

    def init(self):
        self.addLabel((80, 30), (150, 30), 'Food Poison GA')
        self.m_fpsLabel = self.addLabel((400, 30), (150, 30), 'FPS: ##')
        self.addButton((725, 40), (100, 50), 'Back', self.gotoMetamap)
        #self.addImage((725, 550), (50, 50), "assets/imageqt.png")

    def updateTime(self, dt):
        if dt != 0:
            self.m_fpsLabel.setText('FPS: ' + ('%.2f' % (1000/dt)))
            print(dt)
        super().updateTime(dt)

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)