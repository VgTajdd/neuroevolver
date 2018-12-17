import pygame
import screen_manager

class ScreenBase(pygame.sprite.LayeredDirty):
    def __init__(self, width, height, color):
        pygame.sprite.LayeredDirty.__init__(self)

        '''pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('chimp.bmp', -1)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()'''

        self.m_type = screen_manager.ScreenType.DEFAULT;

    def updateTime(self, dt):
        #print(dt)
        pass #necessary because methods needs to be at least one line length

    def onKeyPress(self, key):
        print(key)

    def onMouseMove(self, event):
        pass

    def onMouseDown(self, event):
        print(event)
        pass

    def onMouseRelease(self, event):
        pass