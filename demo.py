import pygame
from screen_manager import ScreenManager
from enums import ScreenType

APP_WIDTH = 800
APP_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
done = False

clock = pygame.time.Clock()
last_tick = pygame.time.get_ticks()

m_screenManager = ScreenManager(APP_WIDTH, APP_HEIGHT)
m_screenManager.gotoScreen(ScreenType.MAIN_MENU)

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 20)
textsurface = myfont.render('Demo', False, (0, 0, 0))

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
        
        screen.blit(textsurface,(0,0))

        pygame.display.update(dirtyRects) #pygame.display.flip()
