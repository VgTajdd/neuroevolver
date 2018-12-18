from actor import Actor
from pygame.font import Font
import colors

class Control(Actor):
    def __init__(self, pos, size, color = colors.WHITE, layer = 1):
        Actor.__init__(self, pos, size, color, layer)
        self.m_mouseEventsEnabled = False

    def mouseEventsEnabled(self):
        return self.m_mouseEventsEnabled

    def setMouseEventsEnabled(self, value):
        self.m_mouseEventsEnabled = value

    def updateTime(self, dt):
        pass #necessary because methods needs to be at least one line length

    def onKeyPress(self, key):
        pass #necessary because methods needs to be at least one line length

    def onMouseMove(self, event):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseRelease(self, event):
        pass

class Button(Control):
    def __init__(self, pos, size, color = colors.WHITE, layer = 1):
        Control.__init__(self, pos, size, color, layer)
        Control.setMouseEventsEnabled(self, True)
        self.m_isPressed = False
        self.m_text = ''

    def setPressed(self, pressed):
        self.m_isPressed = pressed
        if pressed: self.m_color = colors.WHITE
        else:       self.m_color = colors.RED
        self._updateImage()
        self._updateText()

    def setText(self, text):
        self.m_text = text
        self._updateImage() #self.dirty = 1
        self._updateText()

    def _updateText(self):
        if self.m_text:
            font = Font("assets/OpenSans-Regular.ttf", 16)
            textsurface = font.render(self.m_text, False, colors.BLACK) #screen.blit(textsurface,(0,0))
            self.image.blit(textsurface, 
                ((self.image.get_rect().width - textsurface.get_rect().width)/2,
                    (self.image.get_rect().height - textsurface.get_rect().height)/2))

    def setImage(self, imagePath):
        self._updateText()
        self.dirty = 1

    def isPressed(self):
        return self.m_isPressed

    def onMouseDown(self, event):
        if self.rect.collidepoint(event.pos):
            self.setPressed(True)

    def onMouseRelease(self, event):
        if self.isPressed():
            self.setPressed(False)
        if self.rect.collidepoint(event.pos):
            self.onClicked()

    def onClicked(self):
        pass

    def resize(self, w, h):
        super().resize(w, h)
        self._updateText()

#Create Label