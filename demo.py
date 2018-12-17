import pygame
import screen_manager
from enums import ScreenType

APP_WIDTH = 800
APP_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
done = False

clock = pygame.time.Clock()

#timer_resolution = pygame.TIMER_RESOLUTION
#print(timer_resolution)

last_tick = pygame.time.get_ticks()

m_screenManager = screen_manager.ScreenManager(APP_WIDTH, APP_HEIGHT)
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

        m_screenManager.draw(screen)

        pygame.display.flip()