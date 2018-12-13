import pygame

class ScreenManager(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        #self.image, self.rect = load_image('chimp.bmp', -1)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def updateTime(self, dt):
        print(dt)