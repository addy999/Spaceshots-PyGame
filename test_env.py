import pygame
import os, sys
import math
import numpy as np
sys.path.append('./astron')
from game import *

screen_x, screen_y = 1920, 1080

############# LEVEL 1 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 1000)
orbit = Orbit(a=800, b=300, center_x=screen_x*0.75, center_y=screen_x*0.25, CW=True, angular_step = 2*np.pi/(200.0), progress = np.pi/3)
planet = Planet('Test', mass = 4e16, orbit = orbit)
level1 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([0,0], [0, screen_x/5]), win_velocity = 190.0,
           background = (0.0, 0.0, 0.0)
)

############# LEVEL 3 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 1000)
orbit = Orbit(a=800, b=300, center_x=screen_x*0.75, center_y=screen_x*0.25, CW=True, angular_step = 2*np.pi/(200.0), progress = np.pi/3)
planet = Planet('Test', mass = 4e16, orbit = orbit)
level3 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([0,0], [0, screen_x/5]), win_velocity = 190.0,
           background = r'C:\Users\addym\Documents\Gravity Assists\astron\images\stars_2.jpg'
)
##################################

game = Game(scenes = [level1, level3], fullscreen=True, fps=60)
game.startGame()