__name__ = 'astron'
__version__ = '0.1.9.3'

import sys, os

modpath = os.path.abspath(os.path.split(sys.argv[0])[0])
sys.path.append(modpath)

from .pre_made import game
# game.startGame(splash=False)
