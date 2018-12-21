import pygame

class SimulationBase():
    def __init__(self, container, width, height):
        self.m_width = width
        self.m_height = height
        self.m_container = container
        self.m_actors = []

    def draw(self, screen):
        return pygame.sprite.LayeredDirty.draw(self.m_container, screen)

    def updateTime(self, dt):
        for actor in self.m_actors:
            actor.update(dt)

    def forceRedraw(self):
        for actor in self.m_actors:
            actor.dirty = 1

    def addActor(self, actor):
        self.m_container.add(actor)
        self.m_actors.append(actor)

    def free(self):
        self.m_container = None
        self.m_actors.clear()
        self.m_actors = None