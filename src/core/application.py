## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## application.py                                                            ##
## ========================================================================= ##

import pygame
import settings
from gui.screen_manager import ScreenManager
from enums import ScreenType, SimulationType

class Application(object):
    def __init__(self):
        pygame.init() #pygame.font.init() is called here

        icon = pygame.image.load('assets/brain.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('NEUROEVOLVER')

        self.screen = pygame.display.set_mode((settings.APP_WIDTH, settings.APP_HEIGHT), pygame.DOUBLEBUF)
        settings.OBJ_SURFACE = self.screen

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()

        self.m_screenManager = ScreenManager(settings.APP_WIDTH, settings.APP_HEIGHT)

        loadAssets()

    def play(self):
        self.m_screenManager.gotoScreen(ScreenType.MAIN_MENU)
        #self.m_screenManager.gotoScreen(ScreenType.SIMULATION, {'simulationType': SimulationType.NEAT_B2D_WALKER})
        self.onLoop()

    def onLoop(self):

        forceToRepaintAllScreen = False
        is_running = True

        while is_running:
            # limits updates to settings.APP_FPS(=60) frames per second (FPS)
            self.clock.tick(settings.APP_FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                    or event.type == settings.NEAT_IP_EVENT_END_EVOLVING \
                    or event.type == settings.NEAT_DYCICLE_EVENT_END_EVOLVING \
                    or event.type == settings.NEAT_DIP_EVENT_END_EVOLVING \
                    or event.type == settings.NEAT_WALKER_EVENT_END_EVOLVING \
                    or event.type == settings.NEAT_TIP_EVENT_END_EVOLVING:
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    self.m_screenManager.onKeyPress(event.key)
                    if event.key == pygame.K_1:
                        settings.SHOW_DEBUG_SHAPES = not settings.SHOW_DEBUG_SHAPES
                        forceToRepaintAllScreen = True
                if event.type == pygame.KEYUP:
                    self.m_screenManager.onKeyRelease(event.key)
                if event.type == pygame.MOUSEMOTION:
                    self.m_screenManager.onMouseMove(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.m_screenManager.onMouseDown(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.m_screenManager.onMouseRelease(event)
                if event.type == pygame.VIDEOEXPOSE:
                    self.m_screenManager.forceRedraw()

            actual_tick = pygame.time.get_ticks()
            self.m_screenManager.updateTime(actual_tick - self.last_tick)
            self.last_tick = actual_tick
            dirtyRects = self.m_screenManager.draw(self.screen)

            if forceToRepaintAllScreen:
                forceToRepaintAllScreen = False
                pygame.display.flip()
                continue

            if settings.SHOW_DEBUG_SHAPES:
                pygame.display.flip()
            else:
                pygame.display.update(dirtyRects)

        #pygame.quit()
        #sys.exit()

        if len(settings.TRAIN_MODE) != 0:
            tm = settings.TRAIN_MODE
            settings.TRAIN_MODE = ''
            settings.TRAIN_CALLBACK(tm)

    def trainNeatIP(self, genomes, config, currentStep):
        params = {}
        params['isTraining'] = True
        params['currentStep'] = currentStep
        params['genomes'] = genomes
        params['config'] = config
        params['simulationType'] = SimulationType.NEAT_INVERTED_PENDULUM
        self.m_screenManager.gotoScreen(ScreenType.SIMULATION, params)
        self.onLoop()

    def trainNeatDIP(self, genomes, config, currentStep):
        params = {}
        params['isTraining'] = True
        params['currentStep'] = currentStep
        params['genomes'] = genomes
        params['config'] = config
        params['simulationType'] = SimulationType.NEAT_B2D_DIP
        self.m_screenManager.gotoScreen(ScreenType.SIMULATION, params)
        self.onLoop()

    def trainNeatTIP(self, genomes, config, currentStep):
        params = {}
        params['isTraining'] = True
        params['currentStep'] = currentStep
        params['genomes'] = genomes
        params['config'] = config
        params['simulationType'] = SimulationType.NEAT_B2D_TIP
        self.m_screenManager.gotoScreen(ScreenType.SIMULATION, params)
        self.onLoop()

    def trainNeatDycicle(self, genomes, config, currentStep):
        params = {}
        params['isTraining'] = True
        params['currentStep'] = currentStep
        params['genomes'] = genomes
        params['config'] = config
        params['simulationType'] = SimulationType.NEAT_DYCICLE
        self.m_screenManager.gotoScreen(ScreenType.SIMULATION, params)
        self.onLoop()

    def trainNeatWalker(self, genomes, config, currentStep):
        params = {}
        params['isTraining'] = True
        params['currentStep'] = currentStep
        params['genomes'] = genomes
        params['config'] = config
        params['simulationType'] = SimulationType.NEAT_B2D_WALKER
        self.m_screenManager.gotoScreen(ScreenType.SIMULATION, params)
        self.onLoop()

def loadAssets():
    if settings.ASSETS_LOADED:
        return

    def loadImage(path):
        settings.IMAGES_ALPHA[path] = pygame.image.load(path).convert_alpha()
        settings.IMAGES[path] = pygame.image.load(path).convert()

    loadImage('assets/black_btn.png')

    settings.ASSETS_LOADED = True