import pygame

class Box(pygame.sprite.DirtySprite):
    def __init__(self, pos, layer):
        pygame.sprite.DirtySprite.__init__(self) #call DirtySprite intializer
        #self.image, self.rect = load_image('chimp.bmp', -1)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([50, 50])

        color = (255,0,255)
        if layer == 1:
                color = (255,0,0)
        elif layer == 2:
                color = (0,255,0)
        elif layer == 3 :
                color = (0,0,255)

        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

        # Necessary vars.
        self.rect.midtop = pos
        self.dirty = 2
        self.visible = 1
        self._layer = layer


APP_WIDTH = 800
APP_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
done = False

clock = pygame.time.Clock()

#timer_resolution = pygame.TIMER_RESOLUTION
#print(timer_resolution)

last_tick = pygame.time.get_ticks()

allsprites = pygame.sprite.LayeredDirty()

while not done:
        # limits updates to 30 frames per second (FPS)
        clock.tick(30)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                        box = Box(event.pos, event.button)
                        allsprites.add(box)
        
        print(pygame.time.get_ticks() - last_tick)
        last_tick = pygame.time.get_ticks()
        
        dirty=allsprites.draw(screen)
        pygame.display.update(dirty)
        #allsprites.draw(screen)
        #pygame.display.flip()
