import os.path
import pygame

RESOURCES_DIR = 'data'

def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))

class PlayerMini():

    def __init__(self, pos):
        self.image = load_image('playermini.png').convert_alpha()
        #key = (155,155,155)
        #self.image.set_colorkey(key)

        #self.image.fill(self.image.get_rect(), key)
        #self.set_colorkey(key)
        self.position = pos

    def update(self, positionx, positiony):
        #self.image.set_alpha(255)
        self.position = [(positionx * 0.04) - 3 + 10, ((positiony* 0.04) + 421 - 5 - 10)]

    def draw(self, screen):
        screen.blit(self.image,self.position)

class MiniMap():

    def __init__(self, pos):
        self.image = load_image('minimap.png').convert_alpha()
        alpha = 255
        #print alpha
        self.image.set_alpha(alpha)
        #key = (155,155,155)
        #self.image.set_colorkey(key)

        #self.image.fill(self.image.get_rect(), key)
        #self.set_colorkey(key)
        self.position = pos

    def update(self, now, screen_rect, dt):
        #self.image.set_alpha(255)
        self.rect.topleft = self._position

    def draw(self, screen):
        screen.blit(self.image,self.position)