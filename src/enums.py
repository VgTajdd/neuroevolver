from enum import IntEnum

class ScreenType(IntEnum):
    DEFAULT = 0
    MAIN_MENU = 1
    SIMULATION = 2

class SteeringBehaviourType(IntEnum):
    STATIC = 0
    SEEK = 1,
    FLEE = 2,
    PURSUIT = 3,
    EVADE = 4