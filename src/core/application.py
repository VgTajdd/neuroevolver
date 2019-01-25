import pygame
import sys
import settings
from gui.screen_manager import ScreenManager
from enums import ScreenType, SimulationType

class Application(object):
    def __init__(self):
        pygame.init() #pygame.font.init() is called here
        self.screen = pygame.display.set_mode((settings.APP_WIDTH, settings.APP_HEIGHT))
        settings.OBJ_SURFACE = self.screen

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()

        self.m_screenManager = ScreenManager(settings.APP_WIDTH, settings.APP_HEIGHT)

    def play(self):
        self.m_screenManager.gotoScreen(ScreenType.MAIN_MENU)
        self.onLoop()

    def onLoop(self):

        forceToRepaintAllScreen = False
        is_running = True

        while is_running:
            # limits updates to settings.APP_FPS(=60) frames per second (FPS)
            self.clock.tick(settings.APP_FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == settings.NEATIP_EVENT_END_TRAINING_STEP or event.type == settings.NEAT_DYCICLE_EVENT_END_TRAINING_STEP:
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

    def trainNeatIP(self, genomes, config, currentStep):
        params = {}
        params['isTraining'] = True
        params['currentStep'] = currentStep
        params['genomes'] = genomes
        params['config'] = config
        params['simulationType'] = SimulationType.NEAT_INVERTED_PENDULUM
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