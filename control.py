from actor import Actor
from pygame.font import Font
import colors

class Control(Actor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        Actor.__init__(self, pos, size, color, imagePath, alpha, layer)
        self.m_mouseEventsEnabled = False
        self.m_text = ''
        self.m_textColor = colors.BLACK

    def mouseEventsEnabled(self):
        return self.m_mouseEventsEnabled

    def setMouseEventsEnabled(self, value):
        self.m_mouseEventsEnabled = value

    def updateTime(self, dt):
        pass # necessary because methods needs to be at least one line length

    def onKeyPress(self, key):
        pass

    def onMouseMove(self, event):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseRelease(self, event):
        pass

    def setText(self, text):
        self.m_text = text
        self.repaint()

    def setTextColor(self, color):
        self.m_textColor = color
        self.repaint()

    def _updateText(self):
        if self.m_text:
            font = Font("assets/OpenSans-Regular.ttf", 16)
            textsurface = font.render(self.m_text, True, self.m_textColor)
            self.image.blit(textsurface, #screen.blit(textsurface,(0,0))
                ((self.image.get_rect().width - textsurface.get_rect().width)/2,
                    (self.image.get_rect().height - textsurface.get_rect().height)/2))

    def repaint(self):
        super().repaint()   # updates surface and make self dirty = 1.
        self._updateText()  # draws text in current surface.

class Button(Control):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        Control.__init__(self, pos, size, color, imagePath, alpha, layer)
        Control.setMouseEventsEnabled(self, True)
        self.m_isPressed = False
        self.m_callback = None

    def setPressed(self, pressed):
        self.m_isPressed = pressed
        if pressed: self.m_color = colors.GREY_BLUE
        else:       self.m_color = colors.WHITE
        self.repaint()

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
        if self.m_callback != None:
            self.m_callback()

    def setCallback(self, callback):
        self.m_callback = callback

class Label(Control):
    def __init__(self, pos, size, text, color = colors.WHITE, alpha = 0, layer = 1):
        Control.__init__(self, pos, size, color = color, alpha = alpha, layer = layer)
        Control.setText(self, text)

    def updateTime(self, dt):
        self.setPosition(self.m_position[0] + 1, self.m_position[1])

class Image(Control):
    def __init__(self, pos, size, imagePath, color = colors.WHITE, alpha = 255, layer = 1):
        Control.__init__(self, pos, size, color, imagePath, alpha, layer)

    def updateTime(self, dt):
        self.setPosition(self.m_position[0], self.m_position[1] + 1)