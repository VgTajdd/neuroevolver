## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## hud_neat_ip.py                                                            ##
## ========================================================================= ##

from core.hud_base import HudBase
from enums import ScreenType
import core.utils
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
                          str(self.params['currentStep']) + "/" + str(settings.NEAT_IP_EVOLVING_STEPS))
        else:
            imgPath = 'net_neat_ip.png'
            if core.utils.existsFile(imgPath):
                size = core.utils.getImageSize(imgPath)
                self.addImage(((size[0]/2) + 30, (size[1]/2) + 30), size, imgPath)
            self.addButton((770, 15), (60, 30), 'Back', self.gotoMetamap, alpha = 200)

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)