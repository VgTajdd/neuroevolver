import pygame

class SimulationBase():
    def __init__(self, container, width, height):
        self.m_width = width
        self.m_height = height
        self.m_actorManager = SimulationActorManager(self, container)
        self.m_container = container
        self.m_debugContainer = []

    def draw(self, screen):
        return pygame.sprite.LayeredDirty.draw(self.m_container, screen)

    def update(self, dt):
        self.m_debugContainer.clear()
        self.m_actorManager.update(dt)

    def forceRedraw(self):
        self.m_actorManager.forceRedraw()

    def addActor(self, actor):
        self.m_actorManager.addActor(actor)

    def removeActor(self, actor):
        self.m_actorManager.removeActor(actor)

    def free(self):
        self.m_container = None
        self.m_actorManager.free()
        self.m_actorManager = None
        self.m_debugContainer.clear()
        self.m_debugContainer = None

from core.actor import Actor
import core.colors as colors

class SimulationActor(Actor):
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        Actor.__init__(self, pos, size, color, imagePath, alpha, layer)
        self.m_health = 0
        self.m_state = 0
        self.m_isAwaitingToDelete = False

    def setAwaitingToDelete(self, value):
        self.m_isAwaitingToDelete = value

    def addHealth(self, hp):
        self.m_health += hp

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

    def removeActor(self, actor):
        self.m_container.remove(actor)
        self.m_actors.remove(actor)

    def free(self):
        self.m_container = None
        for actor in self.m_actors:
            actor.free()
        self.m_actors.clear()
        self.m_actors = None