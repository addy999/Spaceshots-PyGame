import pygame
import os, sys
import math
import numpy as np
modpath = os.path.abspath(os.path.split(sys.argv[0])[0])
sys.path.append(modpath)

from .game import *

# lines = 0
# files = ['assests', 'game', 'scene', 'utilities']
# for file in files:
#         f = open(r'./astron/' + file + '.py', 'r').read()
#         lines += f.count('\n')
# print(lines)

# screen_x, screen_y = 1920, 1080
screen_x, screen_y = 1366, 768


############# LEVEL 1 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 600)
orbit = Orbit(a=screen_x*500/1920, b=screen_y*500/1080, center_x=screen_x, center_y=screen_y/2, CW=True, angular_step = 2*np.pi/(200.0), progress = np.pi/2)
planet = Planet('Test', mass = 3e16, orbit = orbit)
level1 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([0,0], [screen_x, 0]), win_velocity = 90.0,
           background = (0.0, 0.0, 0.0)
)

############# LEVEL 2 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 550)
orbit = Orbit(a=screen_x*1000/1920, b=screen_y*800/1080, center_x=screen_x/2, center_y=0.0, CW=False, angular_step = 2*np.pi/(200.0), progress = np.pi*0.9)
planet = Planet('Test', mass = 4e16, orbit = orbit, color = (100,0,0))
level2 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([screen_x,0], [screen_x, screen_y/10]), win_velocity = 90.0,
        #    background = modpath + '\images\stars_1.jpg'
        background = getModpath() + r'/images/stars_1.jpg'
)

############# LEVEL 3 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 350)
orbit = Orbit(a=screen_x*800/1920, b=screen_y*300/1080, center_x=screen_x*0.75, center_y=screen_x*0.25, CW=True, angular_step = 2*np.pi/(200.0), progress = np.pi/4)
planet = Planet('Test', mass = 4e16, orbit = orbit, color = (245, 66, 239))
level3 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([0,0], [0, screen_y/5]), win_velocity = 190.0,
           background = getModpath() + r'/images/stars_2.jpg'
)

############# LEVEL 4 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 4500, gas_level = 450)

orbit = Orbit(a=screen_y*800/1080, b=screen_y*800/1080, center_x=0.0, center_y=3*screen_y/4, CW=False, angular_step = np.pi/(200.0), progress = 0.0)
planet = Planet('1', mass = 4e16, orbit = orbit, color = (48, 227, 240))

orbit2 = Orbit(a=screen_y*800/1080, b=screen_y*800/1080, center_x=screen_x, center_y=screen_y/2, CW=True, angular_step = 3*np.pi/(200.0), progress = np.pi/2)
planet2 = Planet('2', mass = 5e16, orbit = orbit2, color=(240, 217, 43))

level4 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet, planet2], win_region = ([screen_x,0], [screen_x, screen_y/7]), win_velocity = 150,
           background = getModpath() + r'/images/stars_3.jpg'
)

############# LEVEL 5 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 5500, gas_level = 250)

orbit = Orbit(a=screen_y*800/1080, b=screen_y*800/1080, center_x=0.0, center_y=3*screen_y/4, CW=False, angular_step = np.pi/(200.0), progress = 0.0)
planet = Planet('Test', mass = 5e16/1.4, orbit = orbit)

orbit2 = Orbit(a=screen_y*800/1080, b=screen_y*800/1080, center_x=screen_x+100, center_y=screen_y/2, CW=True, angular_step = 3*np.pi/(200.0), progress = np.pi/2)
planet2 = Planet('Test', mass = 10e16/1.4, orbit = orbit2)

level5 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet, planet2], 
                   win_region = ([screen_x*0.75,0], [screen_x, 0.0]),
                   win_velocity = 100,
           background = getModpath() + r'/images/stars_4.jpg'
)
##################################

sc = Spacecraft('Test', mass = 100, thrust_force = 5500, gas_level = 250)

orbit = Orbit(a=screen_y*800/1080, b=screen_y*800/1080, center_x=0.0, center_y=3*screen_y/4, CW=False, angular_step = np.pi/(200.0), progress = 0.2)
planet = Planet('Test', mass = 5e16/1.4, orbit = orbit, color = (8, 204, 15))

orbit2 = Orbit(a=screen_y*800/1080, b=screen_y*800/2080, center_x=screen_x/2, center_y=0, CW=False, angular_step = 3*np.pi/(100.0), progress = np.pi*1.5)
planet2 = Planet('Test', mass = 8e16/1.4, orbit = orbit2, color = (255, 162, 0))

level6 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet, planet2], 
                   win_region = ([screen_x*0.75,0], [screen_x, 0.0]),
                   win_velocity = 100, 
           background = getModpath() + r'/images/stars_6.jpg', sc_start_pos = [0.0, screen_y]
)
##################################

game = Game(scenes = [
        level1, 
        level2, 
        level6,
        level3, 
        level4,
        level5,        
        ], fullscreen=True, fps=60)

# game.startGame(splash=True)