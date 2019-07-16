import pygame
import os, sys
import math
import numpy as np
sys.path.append('./astron')
from game import *


############# LEVEL 1 #############

sc = Spacecraft('Test', 100, thrust_force = 3000, gas_level = 1000)
orbit = Orbit(300, 100, 500*0.75, 500*0.3, CW=True, angular_step = 2*np.pi/(200.0*60.0), progress = np.pi/2)
planet = Planet('Test', mass = 2e16, orbit = orbit)
level1 = GameScene((500,500), sc, [planet], win_region = ([100,0], [400, 0]))

##################################

game = Game(scenes = [level1])
game.startGame()