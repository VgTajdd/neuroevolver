## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## hud_b2d.py                                                                ##
## ========================================================================= ##

from core.hud_base import HudBase
from enums import ScreenType, SimulationType
from core.utils import getPathWithoutExtension, existsFile, getImageSize
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
                          str(self.params['currentStep']) + "/" + str(settings.NEAT_DIP_EVOLVING_STEPS))
        else:
            imgPath = self.params['genomePath']
            imgPath = getPathWithoutExtension(imgPath) + '.png'
            if existsFile(imgPath):
                size = getImageSize(imgPath)
                w, h = size
                if size[0] > 450:
                    w = 450
                if size[1] > 450:
                    h = 450
                self.addImage(((w/2) + 30, (h/2) + 30), (w, h), imgPath)
            self.addButton((770, 15), (60, 30), 'Back', self.gotoMetamap, alpha = 200)
            self.addButton((670, 15), (60, 30), 'Reset', self.resetDIP, alpha = 200)

    def resetDIP(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_B2D_DIP})

class HudB2DNEATTIP(HudB2D):
    def __init__(self, width, height, params):
        self.params = params
        HudB2D.__init__(self, width, height)

    def init(self):
        self.showFPS()
        self.addLabel((75, 15), (150, 30), 'NEAT TIP')
        if 'isTraining' in self.params and self.params['isTraining']:
            self.addLabel((75, 45), (150, 30),
                          str(self.params['currentStep']) + "/" + str(settings.NEAT_TIP_EVOLVING_STEPS))
        else:
            imgPath = 'net_neat_tip.png'
            if existsFile(imgPath):
                size = getImageSize(imgPath)
                self.addImage(((size[0]/2) + 30, (size[1]/2) + 30), size, imgPath)
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
                          str(self.params['currentStep']) + "/" + str(settings.NEAT_WALKER_EVOLVING_STEPS))
        else:
            imgPath = 'net_neat_walker.png'
            if existsFile(imgPath):
                size = getImageSize(imgPath)
                self.addImage(((size[0]/2) + 30, (size[1]/2) + 30), size, imgPath)
            self.addButton((770, 15), (60, 30), 'Back', self.gotoMetamap, alpha = 200)