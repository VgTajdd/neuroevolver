import pygame
from screen_base import ScreenBase
from control import Label
from control import Button
import colors

class HudBase(ScreenBase):
    def __init__(self, width, height, color = colors.WHITE):
        ScreenBase.__init__(self, width, height, color)

    def addText(self, pos, size, text):
        label = Label(pos, size, text, layer = 100)
        self.addControl(label)

    def addButton(self, pos, size, text, callback, color = colors.WHITE):
        btn = Button(pos, size, color = color, layer = 100)
        btn.setText(text)
        btn.setCallback(callback)
        self.addControl(btn)