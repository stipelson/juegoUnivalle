import os.path
import pygame

RESOURCES_DIR = 'data'

def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))

class Cancha(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('cancha-techo.png').convert()
        key = (155,155,155)
        self.image.set_colorkey(key)

        #self.image.fill(self.image.get_rect(), key)
        #self.set_colorkey(key)
        self._position = pos
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width, self.rect.height)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, now, screen_rect, dt):
        self.image.set_alpha(255)
        self.rect.topleft = self._position

    def collide_trans(self):
        """ If called after an update, the sprite can move back
        """
        alpha = 255
        self.image.fill((255, 255, 255, alpha), None)

    def normal(self):
        """ If called after an update, the sprite can move back
        """
        alpha = 90
        #print alpha
        self.image.set_alpha(alpha)

class CanchaViga(pygame.sprite.Sprite):

    def __init__(self, pos, tipo):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('viga'+tipo+'Cancha.png').convert_alpha()
        #key = (155,155,155)
        #self.image.set_colorkey(key)

        #self.image.fill(self.image.get_rect(), key)
        #self.set_colorkey(key)
        self._position = pos
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width, self.rect.height)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, now, screen_rect, dt):
        #self.image.set_alpha(255)
        self.rect.topleft = self._position


