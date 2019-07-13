import pygame
import os, sys
import math
sys.path.append('./')
from assests import *
from utilities import *

class Scenario:
    
    def __init__(self, size, spacecraft, planets, sc_start_pos = None, initial_orbit_progress = None):
        
        self.size = size
        self.sc = spacecraft
        self.planets = planets
        self.sc_start_pos = sc_start_pos
        self.initial_orbit_progress = initial_orbit_progress
        
        if not self.sc_start_pos:
            self.sc_start_pos = self._makeScStartPos()
        if not self.initial_orbit_progress:
            self.initial_orbit_progress = {}
            for planet in planets:
                self.initial_orbit_progress.update({
                    planet : 0.0
                })
                
        self.resetPos()
        
    def _makeScStartPos(self):
        
        '''
        Default starting position assumed to be bottom centre of screen
        '''
        
        return self.size[0] / 2, self.size[2]
        
    def resetPos(self):
        
        self.sc.x, self.sc.y = self.sc_start_pos
        
        for planet in self.planets:
            self.planets[self.planets.index(planet)].orbit.progress = self.initial_orbit_progress[planet]
    
    def updateScPos(self, impulse_time):
        
        closes_planet = findClosestPlanet(self.sc, self.planets)
        planet_f = 0.0
        
        if closes_planet:
            planet_f = self.sc.calcGravitationalForce(closes_planet)
                
        self.sc.setNetMomentum(impulse_time, planet_f)
        self.sc.move()
    
def findClosestPlanet(sc, planets):
        
    current_distance = sc.calcDistance(planets[0])
    index_of_closest = 0
    current_index = 0
    for num in range(len(planets)):
        if sc.calcDistance(planets[current_index]) < current_distance: 
            index_of_closest = current_index
            current_distance = sc.calcDistance(planets[current_index])
        current_index += 1
    
    return planets[index_of_closest]