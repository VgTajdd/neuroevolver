from core.screen_base import ScreenBase
from enums import ScreenType
from enums import SimulationType

class Metamap(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP

    def init(self):
        self.addButton((400, 200), (200, 50), 'Demos', self.gotoMetamapDemos)
        self.addButton((400, 300), (200, 50), 'Simulations', self.gotoMetamapSimulations)

        self.addButton((650, 550), (200, 50), 'Back', self.gotoMainMenu)
        self.addLabel((400, 100), (300, 50), 'Choose Mode', alpha = 50)

    def gotoMainMenu(self):
        self.m_manager.gotoScreen(ScreenType.MAIN_MENU)

    def gotoMetamapDemos(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP_DEMOS)

    def gotoMetamapSimulations(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP_SIMULATIONS)

class MetamapDemos(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP_DEMOS

    def init(self):
        self.addButton((400, 200), (200, 50), 'Simple Steering', self.gotoSimpleSteering)
        self.addButton((400, 300), (200, 50), 'Box 2D', self.gotoBox2D)
        self.addButton((400, 400), (200, 50), 'Food Poison GA', self.gotoFPSteering)

        self.addButton((650, 550), (200, 50), 'Back', self.gotoMetamap)
        self.addLabel((400, 100), (300, 50), 'Choose Demo', alpha = 50)

    def gotoSimpleSteering(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.SIMPLE_STEERING})

    def gotoFPSteering(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.FP_STEERING})

    def gotoBox2D(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.B2D})

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)

class MetamapSimulation(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP_SIMULATIONS

    def init(self):
        self.addButton((400, 200), (200, 50), 'NEAT Inv-Pendulum', self.gotoNeatIP)
        self.addButton((400, 300), (200, 50), 'NEAT Dycicle', self.gotoNeatDycicle)
        self.addButton((400, 400), (200, 50), 'NEAT DIP', self.gotoNeatDIP)
        self.addButton((400, 500), (200, 50), 'NEAT Walker', self.gotoNeatWalker)

        self.addButton((650, 550), (200, 50), 'Back', self.gotoMetamap)
        self.addLabel((400, 100), (300, 50), 'Choose Simulation', alpha = 50)

    def gotoNeatIP(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_INVERTED_PENDULUM})

    def gotoNeatDycicle(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_DYCICLE})

    def gotoNeatDIP(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_B2D_DIP})

    def gotoNeatWalker(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_B2D_WALKER})

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)