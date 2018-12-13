import pygame
import screen_manager

APP_WIDTH = 800
APP_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

timer_resolution = pygame.TIMER_RESOLUTION
print(timer_resolution)

last_tick = pygame.time.get_ticks()
sm = screen_manager.ScreenManager(APP_WIDTH, APP_HEIGHT,(250, 250, 250))
allsprites = pygame.sprite.RenderPlain((sm))

while not done:
        # limits updates to 30 frames per second (FPS)
        clock.tick(30)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 3
        if pressed[pygame.K_DOWN]: y += 3
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3
        
        sm.updateTime(pygame.time.get_ticks() - last_tick)
        allsprites.draw(screen)

        #screen.fill((0, 0, 0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
        
        pygame.display.flip()
        #clock.tick(20)
        #print(clock.get_ticks())
        last_tick = pygame.time.get_ticks()