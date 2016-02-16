'''
In this pygame file I (try) to explain how I do basic managment
of (Game?)States. Each State could load a totally different "window"
like a Introscreen, a Logo, a Menu, an Optionscreen, the Game itself etc

This system is far from perfect but it works in a relatively clean way I suppose
Press 1,2,3 to change your state
'''
try:
    import sys, os, random
    import pygame
    from pygame.locals import *
    import os.path
    from pytmx.util_pygame import load_pygame
    import time
    import pyganim
    import itertools
    import pyscroll
    import pyscroll.data
    from pyscroll.group import PyscrollGroup

    from cafeteria import Cafeteria
    from cancha import Cancha
    from cancha import CanchaViga
    from player import Player

except ImportError, err:
    print "Yikes! %s Failed to load Module in Game.py: %s" % (__file__, err)
    sys.exit(1)

RESOURCES_DIR = 'data'
HERO_MOVE_SPEED = 200  # pixels per second
MAP_FILENAME = 'campus.tmx'
TIMER = pygame.time.get_ticks()


def get_map(filename):
    return os.path.join(RESOURCES_DIR, filename)

# Our main Function, this is were everything gets called etc
def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Statemanagment in Pygame")
    global temp_surface
    temp_surface = pygame.Surface((800 /1, 600 /1)).convert()

    # create a timer/clock
    timer1 = pygame.time.Clock()

    # running is true
    running = True

    # Initializes the Statemanager
    # manager.scene is the active State
    # until there is a change(state) event
    # also we pass the screen-Rect for drawing
    # (you could also pass resolution data etc)
    manager = StateMananger(screen)

    while running:
        #Limit the Framerate just for the heck of it
        timer1.tick(50)

        # running is False if handle_events is False (Quit etc)
        running = manager.state.handle_events(pygame.event.get())

        #update and render the managers active state
        manager.update()
        manager.render(screen)

        pygame.display.flip()

    # Say goodbye before you quit
    print 'Quit: See you in Space, Cowboy!'
    pygame.quit()

class StateMananger(object):
    # Statemanager manages States, loads the first state in the
    # constructor and has a option to print things out
    def __init__(self, screen):
        # on constructions change to our first state
        self.change(IntroState(screen))

    def change(self, state):
        # the new self.state is our passed state
        self.state = state
        self.state.manager = self
        # be nice and print what you did
        print ('changed to '+self.get_name())
        print ('('+self.get_descr()+')\n')

    def update(self):
        self.state.update()

    def render(self, screen):
        self.state.render(screen)

    def get_name(self):
        return self.state.name

    def get_descr(self):
        return self.state.description

class State(object):
    # a superclass for our States so we dont have to write things
    # over and over if we want to do sth. in every state we construct.
    def __init__(self, screen):
        self.screen = screen
        self.name = None
        self.description = None

    def __str__(self):
        return str(self.name) + str(self.description)

# After this point there are 3 Scenes defined
# you could do totally different things in each
# I recommend loading those classes from another
# file/module so you don't die a painful death..
class IntroState(State):
    # Our first state
    def __init__(self, screen):
        State.__init__(self, screen)

        self.name = "IntroState"
        self.description = "Playback of the Logos and stuff"

        # A whole Block just to display the Text ...
        self.font1 = pygame.font.SysFont("Monospaced", 50)
        self.font2 = pygame.font.SysFont("Monospaced", 32)
        # Render the text
        self.text1 = self.font1.render(self.name, True, (255,255, 255), (159, 182, 205))
        self.text2 = self.font2.render(self.description, True, (255,255, 255), (159, 182, 205))
        self.text3 = self.font2.render("Press 1, 2, 3 to change States", True, (255,255, 255), (159, 182, 205))
        # Create Text-rectangles
        self.text1Rect = self.text1.get_rect()
        self.text2Rect = self.text2.get_rect()
        self.text3Rect = self.text3.get_rect()

        # Center the Text-rectangles
        self.text1Rect.centerx = self.screen.get_rect().centerx
        self.text1Rect.centery = self.screen.get_rect().centery

        self.text2Rect.centerx = self.screen.get_rect().centerx
        self.text2Rect.centery = self.screen.get_rect().centery+50

        self.text3Rect.centerx = self.screen.get_rect().centerx
        self.text3Rect.centery = self.screen.get_rect().centery+100

    def render(self, screen):
        # Rendering the State
        pygame.display.set_caption(self.name +"  "+self.description)
        screen.fill((20, 20, 20))

        self.screen.blit(self.text1, self.text1Rect)
        self.screen.blit(self.text2, self.text2Rect)
        self.screen.blit(self.text3, self.text3Rect)

    def update(self):
        pass

    def handle_events(self,events):
        # every State has its own eventmanagment
        for e in events:
            if e.type == QUIT:
                print ("Pressed Quit (Window)")
                return False

            elif e.type == KEYDOWN:

                if e.key == K_ESCAPE:
                    print ("Pressed Quit (Esc)")
                    return False
                # change State if user presses "2"
                if e.key == K_2:
                    # This is the changecommand. You could also change via
                    # timer or other stuff.
                    self.manager.change(MenuState(self.screen))
                if e.key == K_3:
                    self.manager.change(Gametate(self.screen))
        return True

class MenuState(State):
    # Your Menu could be here
    def __init__(self, screen):
        State.__init__(self, screen)

        self.name = "MenuState"
        self.description = "Gamemenu"

        # A whole Block just to display the Text ...
        self.font1 = pygame.font.SysFont("Monospaced", 50)
        self.font2 = pygame.font.SysFont("Monospaced", 32)
        # Render the text
        self.text1 = self.font1.render(self.name, True, (255,255, 255), (159, 182, 205))
        self.text2 = self.font2.render(self.description, True, (255,255, 255), (159, 182, 205))
        # Create Text-rectangles
        self.text1Rect = self.text1.get_rect()
        self.text2Rect = self.text2.get_rect()

        # Center the Text-rectangles
        self.text1Rect.centerx = self.screen.get_rect().centerx
        self.text1Rect.centery = self.screen.get_rect().centery

        self.text2Rect.centerx = self.screen.get_rect().centerx
        self.text2Rect.centery = self.screen.get_rect().centery+50

    def render(self, screen):
        # Rendering the State
        pygame.display.set_caption(self.name +"  "+self.description)
        screen.fill((20, 20, 20))

        self.screen.blit(self.text1, self.text1Rect)
        self.screen.blit(self.text2, self.text2Rect)

    def update(self):
        pass

    def handle_events(self,events):
        # every State has its own eventmanagment
        for e in events:
            if e.type == QUIT:
                print ("Pressed Quit (Window)")
                return False

            elif e.type == KEYDOWN:

                if e.key == K_ESCAPE:
                    print ("Pressed Quit (Esc)")
                    return False
                # change State if user presses "1"
                if e.key == K_1:
                    self.manager.change(IntroState(self.screen))
                # change State if user presses "3"
                if e.key == K_3:
                    self.manager.change(GameState(self.screen))
        return True

class GameState(State):
    # Gamestate - run your stuff inside here (maybe another manager?
    # for your levelmanagment?)
    filename = get_map(MAP_FILENAME)
    def __init__(self, screen):
        State.__init__(self, screen)

        self.name = "GameState"
        self.description = "Draw your game inside here"

        # A whole Block just to display the Text ...
        self.font1 = pygame.font.SysFont("Monospaced", 50)
        self.font2 = pygame.font.SysFont("Monospaced", 32)
        # Render the text
        self.text1 = self.font1.render(self.name, True, (255,255, 255), (159, 182, 205))
        self.text2 = self.font2.render(self.description, True, (255,255, 255), (159, 182, 205))
        # Create Text-rectangles
        self.text1Rect = self.text1.get_rect()
        self.text2Rect = self.text2.get_rect()

        # Center the Text-rectangles
        self.text1Rect.centerx = self.screen.get_rect().centerx
        self.text1Rect.centery = self.screen.get_rect().centery

        self.text2Rect.centerx = self.screen.get_rect().centerx
        self.text2Rect.centery = self.screen.get_rect().centery+50

        self.screen_rect = screen.get_rect()
        self.done = False
        self.fps = 60
        self.done = False
        self.keys = pygame.key.get_pressed()
        # true while running
        self.running = False
         # load data from pytmx
        self.tmx_data = load_pygame(self.filename, pixelalpha=True)
        #print self.tmx_data.layers.TiledTileLayer.properties['under0']
        # setup level geometry with simple pygame rects, loaded from pytmx
        # create new data source for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        w, h = screen.get_size()
        # create new renderer (camera)
        # clamp_camera is used to prevent the map from scrolling past the map's edge
        # cambiar el 1 por el tamano de zoom
        self.map_layer = pyscroll.BufferedRenderer(self.map_data,
                                                   (w / 1, h / 1),
                                                   clamp_camera=True)
        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        #self.hero = Hero()
        # put the hero in the center of the map
        #self.hero.position = self.map_layer.map_rect.center


    def render(self, screen):
        # Rendering the State
        pygame.display.set_caption(self.name +"  "+self.description)
        screen.fill((20, 20, 20))

        self.screen.blit(self.text1, self.text1Rect)
        self.screen.blit(self.text2, self.text2Rect)

    def draw(self, surface):

        # center the map/screen on our Hero
        #self.group.center(self.hero.rect.center)
        # draw the map and all sprites
        self.group.draw(surface)

    def update(self):
        clock = pygame.time.Clock()
        scale = pygame.transform.scale
        self.running = True

        try:
            while self.running:
                dt = clock.tick() / 1000.

                self.draw(temp_surface)
                scale(temp_surface, self.screen.get_size(), self.screen)
                pygame.display.flip()
                #self.clocky.tick(self.fps)
                #self.display_fps()

        except KeyboardInterrupt:
            self.running = False
        pass

    def handle_events(self,events):
        # every State has its own eventmanagment
        for e in events:
            if e.type == QUIT:
                print ("Pressed Quit (Window)")
                return False

            elif e.type == KEYDOWN:

                if e.key == K_ESCAPE:
                    print ("Pressed Quit (Esc)")
                    return False
                # change State if user presses "2"
                if e.key == K_2:
                    self.manager.change(MenuState(self.screen))
                # change State if user presses "1"
                if e.key == K_1:
                    self.manager.change(IntroState(self.screen))
        return True

# Run the main function
if __name__ == "__main__":
    main()