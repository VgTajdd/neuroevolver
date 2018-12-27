from pygame.math import Vector2
from constants.enums import SteeringBehaviourType
from steering import Steering

class SteeringBehaviour():
    def __init__(self, actor):
        self.m_actor = actor
        self.m_components = []

        self.m_arriveEnabled = False
        self.m_arriveDistance = 100
        self.m_arriveFactor = 1.0

    def update(self, dt):
        self.m_arriveEnabled = False

        for component in self.m_components:
            component.update(dt)

        # Hack to implement arrive.
        if len(self.m_components) is 1:
            if self.m_components[0].m_type is SteeringBehaviourType.SEEK:
                self.m_arriveEnabled = True

        if self.m_arriveEnabled:
            if 0.001 < self.m_components[0].m_actualDistanceToTarget < self.m_arriveDistance:
                self.m_arriveFactor = self.m_components[0].m_actualDistanceToTarget / self.m_arriveDistance

    def addComponent(self, type, targetActor = None, targetPosition = None):

        if targetActor is None and targetPosition is None:
            print("Not valid behaviour component added.")
            return

        isNecessaryTargetActor = type is SteeringBehaviourType.PURSUIT or type is SteeringBehaviourType.EVADE

        if targetActor is None and isNecessaryTargetActor:
            print("Not valid behaviour component added.")
            return

        component = BehaviourComponent(type)
        component.m_targetActor = targetActor
        component.m_targetPosition = targetPosition
        component.m_actor = self.m_actor
        self.m_components.append(component)

    def free(self):
        for component in self.m_components:
            component.free()
        self.m_components = None
        self.m_actor = None

class BehaviourComponent():
    def __init__(self, type):
        self.m_targetActor = None
        self.m_targetPosition = None
        self.m_actor = None
        self.m_type = type

        # Constants.
        self.m_steeringConstant = 0.01
        self.m_steeringRadious = 0 #500

        # Temporal vars.
        self.m_actualDistanceToTarget = 0

    def setTargetActor(self, actor):
        self.m_targetActor = actor

    def setTargetPosition(self, x_or_pair, y = None):
        x_input = 0
        y_input = 0
        if y == None:
            x_input = x_or_pair[0]
            y_input = x_or_pair[1]
        else:
            x_input = x_or_pair
            y_input = y
        self.m_targetPosition = x_input, y_input

    def updateTargetPosition(self):
        if self.m_targetActor:
            self.m_targetPosition = self.m_targetActor.m_position

    def update(self, dt):
        #if self.m_type is SteeringBehaviourType.SEEK or self.m_type is SteeringBehaviourType.FLEE:
        self.updateTargetPosition()

        self.m_actualDistanceToTarget = Vector2(self.m_targetPosition).distance_to(self.m_actor.m_position)
        if self.m_steeringRadious > 0:
            if self.m_actualDistanceToTarget > self.m_steeringRadious:
                return

        # If there is a valid target use steering behaviour.
        if self.m_targetPosition:
            if self.m_type == SteeringBehaviourType.SEEK:
                Steering.seek(self.m_actor, self.m_targetPosition, self.m_steeringConstant)
            elif self.m_type == SteeringBehaviourType.FLEE:
                Steering.flee(self.m_actor, self.m_targetPosition, self.m_steeringConstant)
            elif self.m_type == SteeringBehaviourType.PURSUIT:
                Steering.pursuit(self.m_actor, self.m_targetActor, self.m_steeringConstant)
            elif self.m_type == SteeringBehaviourType.EVADE:
                Steering.evade(self.m_actor, self.m_targetActor, self.m_steeringConstant)

    def free(self):
        self.m_targetActor = None
        self.m_targetPosition = None
        self.m_actor = None