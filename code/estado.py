import os.path
import pygame

RESOURCES_DIR = 'data'

def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))

class Estado():

    def __init__(self, pos):
        self.image = load_image('estado.png').convert_alpha()
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