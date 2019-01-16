from core.hud_base import HudBase
from enums import ScreenType
import settings

class HudNeatIP(HudBase):
    def __init__(self, width, height, params):
        self.params = params
        HudBase.__init__(self, width, height)

    def init(self):
        self.showFPS()
        self.addLabel((75, 15), (150, 30), 'NEAT Inv-pendulum')
        if 'isTraining' in self.params and self.params['isTraining']:
            self.addLabel((75, 45), (150, 30),
                          str(self.params['currentStep']) + "/" + str(settings.NEATIP_TRAINING_STEPS))
        else:
            self.addButton((770, 15), (60, 30), 'Back', self.gotoMetamap, alpha = 200)

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)