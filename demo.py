import pygame
from screen_manager import ScreenManager
from enums import ScreenType
import constants

pygame.init() #pygame.font.init() is called here
screen = pygame.display.set_mode((constants.APP_WIDTH, constants.APP_HEIGHT))
done = False

clock = pygame.time.Clock()
last_tick = pygame.time.get_ticks()

m_screenManager = ScreenManager(constants.APP_WIDTH, constants.APP_HEIGHT)
m_screenManager.gotoScreen(ScreenType.MAIN_MENU)

while not done:
        # limits updates to 30 frames per second (FPS)
        clock.tick(30)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN:
                        m_screenManager.onKeyPress(event.key)
                if event.type == pygame.MOUSEMOTION:
                        m_screenManager.onMouseMove(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                        m_screenManager.onMouseDown(event)
                if event.type == pygame.MOUSEBUTTONUP:
                        m_screenManager.onMouseRelease(event)
        
        m_screenManager.updateTime(pygame.time.get_ticks() - last_tick)
        last_tick = pygame.time.get_ticks()

        dirtyRects = m_screenManager.draw(screen)
        pygame.display.update(dirtyRects) #pygame.display.flip()
