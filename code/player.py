import os.path
import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import sys
import time
import pyganim
import itertools
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

# -----------------Variables globales -------------------------

RESOURCES_DIR = 'data'
global SKEL_IMAGE
SKEL_IMAGE = pygame.image.load("data/character.png")
DIRECT_DICT = {pygame.K_LEFT  : (-1, 0),
               pygame.K_RIGHT : ( 1, 0),
               pygame.K_UP    : ( 0,-1),
               pygame.K_DOWN  : ( 0, 1)}

# _----------------------- Funciones -----------------------------

def split_sheet(sheet, size, columns, rows):
    """
    Divide a loaded sprite sheet into subsurfaces.

    The argument size is the width and height of each frame (w,h)
    columns and rows are the integer number of cells horizontally and
    vertically.
    """
    subsurfaces = []
    for y in range(rows):
        row = []
        for x in range(columns):
            rect = pygame.Rect((x*size[0], y*size[1]), size)
            row.append(sheet.subsurface(rect))
        subsurfaces.append(row)
    return subsurfaces

#---------------------------------- Clases ------------------------------

class Player(pygame.sprite.Sprite):
    """
    This class will represent our user controlled character.
    """
    SIZE = (72, 80)

    def __init__(self, pos, speed, facing=pygame.K_RIGHT):
        pygame.sprite.Sprite.__init__(self)
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is in pixels/frame; and facing is the Player's starting
        direction (given as a key-constant).
        """
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.speed = speed
        self.direction = facing
        self.old_direction = None # Player's previous direction every frame.
        self.direction_stack = [] # Held keys in the order they were pressed.
        self.redraw = True # Forces redraw if needed.
        self.animate_timer = 0.0
        self.animate_fps = 7
        self.image = None
        self.walkframes = None
        self.walkframe_dict = self.make_frame_dict()
        self.adjust_images()
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        SKEL_IMAGE.convert_alpha()

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def move_back(self, dt):
        """ If called after an update, the sprite can move back
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frame cycles. We can use
        transform functions to reduce the size of the sprite sheet needed.
        """
        frames = split_sheet(SKEL_IMAGE, Player.SIZE, 12, 1)[0]
        flips = [pygame.transform.flip(frame, True, False) for frame in frames]
        walk_cycles = {pygame.K_LEFT : itertools.cycle(frames[6:8]),
                       pygame.K_RIGHT: itertools.cycle(flips[6:8]),
                       pygame.K_DOWN : itertools.cycle(frames[0:3]),
                       pygame.K_UP   : itertools.cycle(frames[3:5])}
        return walk_cycles

    def adjust_images(self, now=0):
        """
        Update the sprite's walkframes as the sprite's direction changes.
        """
        if self.direction != self.old_direction:
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image(now)

    def make_image(self, now):
        """
        Update the sprite's animation as needed.
        """
        elapsed = now-self.animate_timer > 1000.0/self.animate_fps
        if self.redraw or (self.direction_stack and elapsed):
            self.image = next(self.walkframes)
            self.animate_timer = now
        self.redraw = False



    def add_direction(self, key):
        """
        Add a pressed direction key on the direction stack.
        """
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """
        Pop a released key from the direction stack.
        """
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def get_event(self, event):
        """
        Handle events pertaining to player control.
        """
        if event.type == pygame.KEYDOWN:
            self.add_direction(event.key)
            if event.key == pygame.K_LSHIFT:
                self.speed = 3
            else:
                self.speed = 2
        elif event.type == pygame.KEYUP:
            self.pop_direction(event.key)
            if event.key == pygame.K_LSHIFT:
                self.speed = 2
        #  def update(self, dt):
        # self._old_position = self._position[:]
        # self._position[0] += self.velocity[0] * dt
        # self._position[1] += self.velocity[1] * dt
        # self.rect.topleft = self._position
        # self.feet.midbottom = self.rect.midbottom
    def update(self, now, screen_rect, dt):
        """
        Updates our player appropriately every frame.
        """
        self.adjust_images(now)
        self._old_position = self._position[:]
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

        if self.direction_stack:
            direction_vector = DIRECT_DICT[self.direction]
            self._old_position = self._position[:]
            # movimiento en 8 direcciones
            #self._position[0] += self.velocity[0] * dt
            #self._position[1] += self.velocity[1] * dt
            self._position[0] += self.speed*direction_vector[0]
            self._position[1] += self.speed*direction_vector[1]
            self.rect.topleft = self._position
            self.feet.midbottom = self.rect.midbottom

    def draw(self, surface):
        """
        Draws the player to the target surface.
        """
        surface.blit(self.image, self.rect)