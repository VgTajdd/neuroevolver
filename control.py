from actor import Actor

class Control(Actor):
    def __init__(self, pos, layer = 1):
        Actor.__init__(self, pos, layer)
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
    def __init__(self, pos, layer = 1):
        Control.__init__(self, pos, layer)
        Control.setMouseEventsEnabled(self, True)
        self.m_isPressed = False

    def setPressed(self, pressed):
        self.m_isPressed = pressed
        if pressed: 
            self.image.fill((255,255,0))
        else:
            self.image.fill((255,0,0))
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