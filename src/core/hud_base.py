import pygame
from core.screen_base import ScreenBase
import core.colors as colors

class HudBase(ScreenBase):
    def __init__(self, width, height, color = colors.WHITE):
        self.m_fpsLabel = None
        self.m_fpsBuffer = []
        self.m_showFPS = False
        ScreenBase.__init__(self, width, height, color)

    def showFPS(self):
        if self.m_showFPS: 
            return
        self.m_fpsLabel = self.addLabel((400, 30), (150, 30), 'FPS: 60')
        self.m_showFPS = True

    def hideFPS(self):
        if not self.m_showFPS: 
            return
        self.removeControl(self.m_fpsLabel)
        self.m_fpsLabel = None
        self.m_showFPS = False

    def updateTime(self, dt):
        if dt != 0 and self.m_showFPS:
            self.m_fpsBuffer.append(1000/dt)
            if len(self.m_fpsBuffer) >= 15:
                fpsAverage = sum(self.m_fpsBuffer) / float(len(self.m_fpsBuffer))
                self.m_fpsLabel.setText('FPS: ' + ('%.2f' % fpsAverage))
                self.m_fpsBuffer.clear()

    def free(self):
        self.m_fpsLabel = None
        self.m_fpsBuffer.clear()