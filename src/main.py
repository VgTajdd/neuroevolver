import pygame
from gui.screen_manager import ScreenManager
from enums import ScreenType
import settings

pygame.init() #pygame.font.init() is called here
screen = pygame.display.set_mode((settings.APP_WIDTH, settings.APP_HEIGHT))

clock = pygame.time.Clock()
last_tick = pygame.time.get_ticks()

m_screenManager = ScreenManager(settings.APP_WIDTH, settings.APP_HEIGHT)
m_screenManager.gotoScreen(ScreenType.MAIN_MENU)

forceToRepaintAllScreen = False

is_running = True
while is_running:
    # limits updates to settings.APP_FPS(=60) frames per second (FPS)
    clock.tick(settings.APP_FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            m_screenManager.onKeyPress(event.key)
            if event.key == pygame.K_1:
                settings.SHOW_DEBUG_SHAPES = not settings.SHOW_DEBUG_SHAPES
                forceToRepaintAllScreen = True
        if event.type == pygame.KEYUP:
            m_screenManager.onKeyRelease(event.key)
        if event.type == pygame.MOUSEMOTION:
            m_screenManager.onMouseMove(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_screenManager.onMouseDown(event)
        if event.type == pygame.MOUSEBUTTONUP:
            m_screenManager.onMouseRelease(event)
        if event.type == pygame.VIDEOEXPOSE:
            m_screenManager.forceRedraw()

    actual_tick = pygame.time.get_ticks()
    m_screenManager.updateTime(actual_tick - last_tick)
    last_tick = actual_tick
    dirtyRects = m_screenManager.draw(screen)

    if forceToRepaintAllScreen:
        forceToRepaintAllScreen = False
        pygame.display.flip()
        continue

    if settings.SHOW_DEBUG_SHAPES:
        pygame.display.flip()
    else:
        pygame.display.update(dirtyRects)
