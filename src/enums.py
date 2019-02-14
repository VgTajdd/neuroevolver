from enum import IntEnum

class ScreenType(IntEnum):
    DEFAULT = 0
    MAIN_MENU = 1
    META_MAP = 2
    META_MAP_DEMOS = 3
    META_MAP_SIMULATIONS = 4
    META_MAP_TRAININGS = 5
    SETTINGS = 6
    SIMULATION = 7

class SimulationType(IntEnum):
    NONE = 0
    SIMPLE_STEERING = 1
    FP_STEERING = 2
    NEAT_INVERTED_PENDULUM = 3
    NEAT_DYCICLE = 4
    B2D = 5
    NEAT_B2D_DIP = 6
    NEAT_B2D_WALKER = 7

class SteeringBehaviourType(IntEnum):
    STATIC = 0
    SEEK = 1
    FLEE = 2
    PURSUIT = 3
    EVADE = 4

class NPCType(IntEnum):
    NONE = 0
    FOOD = 1
    POISON = 2

class DebugShape(IntEnum):
    LINE = 0
    RECT = 1
    ELLIPSE = 2
    POLYGON = 3