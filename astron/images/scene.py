import pygame
import os, sys
import math
sys.path.append('./')
from assests import *
from utilities import *


class Scene:
    
    def __init__(self, 
                 spacecraft, 
                 planets, 
                 initial_map = {}, 
                 win_region, 
                 win_velocity, 
                 background = None # Image path / color tuple
                ):
        
        self.sc = spacecraft
        self.planets = planets
        self.win_region = win_region
        self.win_min_velocity = win_velocity
        
        self.resetPos()
        
    def resetPos(self, initial_map):
        
        

class Game:
    
    def __init__(self, resolution, fullscreen = False, font = ('Helvetica Neue', 30), fps = 60.0):
        
        pygame.init()
        pygame.font.init()
        
        
        
        
        # Start screen
        if fullscreen:
            self.screen = pygame.display.set_mode((resolution[0], resolution[1]), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((resolution[0], resolution[1]))
        