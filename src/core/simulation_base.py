import pygame
from pygame.math import Vector2

class SimulationBase():
    def __init__(self, container, width, height):
        self.m_width = width
        self.m_height = height
        self.m_actorManager = SimulationActorManager(self, container)
        self.m_container = container
        self.m_debugContainer = []

    def onKeyPress(self, event):
        pass

    def onKeyRelease(self, event):
        pass
    
    def onMouseMove(self, event):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseRelease(self, event):
        pass

    def draw(self, screen):
        return pygame.sprite.LayeredDirty.draw(self.m_container, screen)

    def update(self, dt):
        self.m_debugContainer.clear()
        self.m_actorManager.update(dt)

    def forceRedraw(self):
        self.m_actorManager.forceRedraw()

    def addActor(self, actor):
        return self.m_actorManager.addActor(actor)

    def removeActor(self, actor):
        self.m_actorManager.removeActor(actor)

    def free(self):
        self.m_container = None
        self.m_actorManager.free()
        self.m_actorManager = None
        self.m_debugContainer.clear()
        self.m_debugContainer = None

class SimulationActorManager():
    def __init__(self, simulation, container):
        self.m_simulationReference = simulation
        self.m_container = container
        self.m_actors = []

    def update(self, dt):
        for actor in self.m_actors:
            if actor.m_isAwaitingToDelete:
                self.m_container.remove(actor)
                self.m_actors.remove(actor)
                actor.free()
                continue
            actor.update(dt)

    def forceRedraw(self):
        #for actor in self.m_actors:
            #actor.dirty = 1
        pass

    def addActor(self, actor):
        self.m_container.add(actor)
        self.m_actors.append(actor)
        return actor

    def removeActor(self, actor):
        self.m_container.remove(actor)
        self.m_actors.remove(actor)

    def free(self):
        self.m_container = None
        for actor in self.m_actors:
            actor.free()
        self.m_actors.clear()
        self.m_actors = None
