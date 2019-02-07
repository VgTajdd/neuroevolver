from core.hud_base import HudBase
from enums import ScreenType
import settings

class HudB2D(HudBase):
    def __init__(self, width, height):
        HudBase.__init__(self, width, height)

    def init(self):
        self.showFPS()
        self.addLabel((80, 30), (150, 30), 'Box2D')
        self.addButton((725, 40), (100, 50), 'Back', self.gotoMetamap)

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)

class HudB2DNEATDIP(HudB2D):
    def __init__(self, width, height, params):
        self.params = params
        HudB2D.__init__(self, width, height)

    def init(self):
        self.showFPS()
        self.addLabel((75, 15), (150, 30), 'NEAT DIP')
        if 'isTraining' in self.params and self.params['isTraining']:
            self.addLabel((75, 45), (150, 30),
                          str(self.params['currentStep']) + "/" + str(settings.NEAT_DIP_TRAINING_STEPS))
        else:
            self.addButton((770, 15), (60, 30), 'Back', self.gotoMetamap, alpha = 200)

class HudB2DNEATWalker(HudB2D):
    def __init__(self, width, height, params):
        self.params = params
        HudB2D.__init__(self, width, height)

    def init(self):
        self.showFPS()
        self.addLabel((75, 15), (150, 30), 'NEAT Walker')
        if 'isTraining' in self.params and self.params['isTraining']:
            self.addLabel((75, 45), (150, 30),
                          str(self.params['currentStep']) + "/" + str(settings.NEAT_WALKER_TRAINING_STEPS))
        else:
            self.addButton((770, 15), (60, 30), 'Back', self.gotoMetamap, alpha = 200)