import pygame
import os, sys
import math
sys.path.append('./')
from assests import *
from scene import *
from utilities import *

class GameScene(Scenario):
    
    def __init__(self, 
                 resolution,
                 sc,
                 planets,
                 sc_start_pos = None, 
                 initial_orbit_progress = None,
                 win_region = tuple, # ([x1,x2], [y1,y2])
                 win_velocity = float,
                 background = None # Image path / color tuple
                ):
        
        super().__init__(self, resolution, sc, planets, sc_start_pos, initial_orbit_progress)
        self.background = background
        self.win_region = win_region
        self.win_min_velocity = win_velocity
        
class Game:
    
    def __init__(self, resolution, fullscreen = False, font = 'Helvetica Neue', font_size = 30, fps = 60.0, scenes = []):
        
        pygame.init()
        pygame.font.init()
        
        self.clock = pygame.time.Clock()
        self.resolution = resolution
        self.fullscreen = fullscreen
        self.fps = fps
        self.scenes = scenes
        
        # Start screen
        if fullscreen:
            self.screen = pygame.display.set_mode((resolution[0], resolution[1]), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((resolution[0], resolution[1]))
    
    def renderBackground(self, scene):
        
        if scene.background:
            if isinstance(scene.background, list) and list(scene.background) == 3:
                # RGB Value
                self.screen.fill(scene.background)
            else:
                # Image path
                img = pygame.image.load(scene.background)
                img_scaled = pygame.transform.scale(img, self.resolution)
                rectangle = img_scaled.get_rect()
                rectangle = rectangle.move((0,0))
                self.screen.blit(img_scaled, rectangle)
                           

