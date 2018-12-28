from enum import IntEnum

class ScreenType(IntEnum):
    DEFAULT = 0
    MAIN_MENU = 1
    META_MAP = 2
    SIMULATION = 3

class SimulationType(IntEnum):
    NONE = 0
    SIMPLE_STEERING = 1
    FP_STEERING = 2

class SteeringBehaviourType(IntEnum):
    STATIC = 0
    SEEK = 1,
    FLEE = 2,
    PURSUIT = 3,
    EVADE = 4