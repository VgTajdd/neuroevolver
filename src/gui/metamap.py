from core.screen_base import ScreenBase
from enums import ScreenType
from enums import SimulationType

class Metamap(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP

    def init(self):
        self.addButton((400, 400), (200, 50), 'Demos', self.gotoMetamapDemos, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 200), (200, 50), 'Simulations', self.gotoMetamapSimulations, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 300), (200, 50), 'Evolver', self.gotoMetamapTrainings, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)

        self.addButton((650, 550), (200, 50), 'Back', self.gotoMainMenu, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addLabel((400, 100), (300, 50), 'Choose Mode', alpha = 200)

    def gotoMainMenu(self):
        self.m_manager.gotoScreen(ScreenType.MAIN_MENU)

    def gotoMetamapDemos(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP_DEMOS)

    def gotoMetamapSimulations(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP_SIMULATIONS)

    def gotoMetamapTrainings(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP_TRAININGS)

class MetamapDemos(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP_DEMOS

    def init(self):
        self.addButton((400, 200), (200, 50), 'Simple Steering', self.gotoSimpleSteering, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 300), (200, 50), 'Box 2D', self.gotoBox2D, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 400), (200, 50), 'Food Poison GA', self.gotoFPSteering, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)

        self.addButton((650, 550), (200, 50), 'Back', self.gotoMetamap, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addLabel((400, 100), (300, 50), 'Choose Demo', alpha = 255)

    def gotoSimpleSteering(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.SIMPLE_STEERING})

    def gotoFPSteering(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.FP_STEERING})

    def gotoBox2D(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.B2D})

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)

import settings
import pygame
import core.colors as colors

class MetamapSimulation(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP_SIMULATIONS

    def init(self):
        self.addButton((400, 280), (200, 50), 'NEAT IP', self.gotoNeatIP, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 360), (200, 50), 'NEAT Dycicle', self.gotoNeatDycicle, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 200), (200, 50), 'NEAT DIP', self.gotoNeatDIP, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 440), (200, 50), 'NEAT Walker', self.gotoNeatWalker, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 520), (200, 50), 'NEAT TIP', self.gotoNeatTIP, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)

        self.addButton((650, 550), (200, 50), 'Back', self.gotoMetamap, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addLabel((400, 100), (300, 50), 'Choose Simulation', alpha = 255)

    def gotoNeatIP(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_INVERTED_PENDULUM})

    def gotoNeatDycicle(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_DYCICLE})

    def gotoNeatDIP(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_B2D_DIP})

    def gotoNeatTIP(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_B2D_TIP})

    def gotoNeatWalker(self):
        self.m_manager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_B2D_WALKER})

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)

class MetamapTraining(ScreenBase):
    def __init__(self, width, height, color):
        ScreenBase.__init__(self, width, height, color)
        self.m_type = ScreenType.META_MAP_TRAININGS

    def init(self):
        self.addButton((400, 280), (200, 50), 'NEAT IP', self.gotoNeatIP, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 360), (200, 50), 'NEAT Dycicle', self.gotoNeatDycicle, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 200), (200, 50), 'NEAT DIP', self.gotoNeatDIP, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 440), (200, 50), 'NEAT Walker', self.gotoNeatWalker, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addButton((400, 520), (200, 50), 'NEAT TIP', self.gotoNeatTIP, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)

        self.addButton((650, 550), (200, 50), 'Back', self.gotoMetamap, imagePath = 'assets/black_btn.png', textColor = colors.WHITE)
        self.addLabel((400, 100), (300, 50), 'Choose Evolution', alpha = 255)

    def gotoNeatIP(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        settings.TRAIN_MODE = settings.NEAT_IP_KEY

    def gotoNeatDycicle(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        settings.TRAIN_MODE = settings.NEAT_DYCICLE_KEY

    def gotoNeatDIP(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        settings.TRAIN_MODE = settings.NEAT_DIP_KEY

    def gotoNeatTIP(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        settings.TRAIN_MODE = settings.NEAT_TIP_KEY

    def gotoNeatWalker(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        settings.TRAIN_MODE = settings.NEAT_WALKER_KEY

    def gotoMetamap(self):
        self.m_manager.gotoScreen(ScreenType.META_MAP)