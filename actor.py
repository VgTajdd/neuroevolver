import pygame

class Actor(pygame.sprite.DirtySprite):
    def __init__(self, pos, layer = 1):
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
        self.dirty = 1
        self.visible = 1
        self._layer = layer

    def setPosition(self, pos):
        self.rect.lefttop = pos