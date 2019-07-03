import sys
import numpy as np
import pygame
sys.path.append('./')
from utilities import *

DEFAULT_SC_SPRITE = r'./images/ship1.png'

class Asset:
    
    def __init__(self, name, x = 0.0, y = 0.0, mass = 0, vel = None):
        
        self.x = x
        self.y = y
        self.name = name
        self.mass = mass
        self.vel = vel
        if not vel:
            self.vel = Velocity(0.0, 0.0)
            
        self._p = Momentum(self.vel.x, self.vel.y, self.mass)
    
    def resetPos(self):
        
        self.x = 0
        self.y = 0
    
    def calcDistance(self, other_asset):
        
        dx = self.x - other_asset.x
        dy = self.y - other_asset.y
        
        return np.sqrt(dx**2 + dy**2)   

    def calcVector(self, other_asset):
        
        dx = other_asset.x - self.x
        dy = other_asset.y - self.y
        
        return dx, dy
    
    def calcGravitationalForce(self, other_asset):
       
        G = 6.67408e-11
        M = self.mass
        m = other_asset.mass
        r = self.calcDistance(other_asset)
        
        mag = G*M*m / r**2
        x,y = self.calcVector(other_asset)
        
        return Force(x, y, mag)
     
    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, val):
        self._p = val
        self.vel = Velocity(val.x / self.mass, val.y / self.mass)
              
class Planet(Asset):
    
    def __init__(self, name, x  = 0.0, y = 0.0, mass = 0.0, orbit = Orbit):
    
        super().__init__(name, x, y, mass)
        self.g = 6.67408e-11 # m^3/kg*s^2
        self.orbit = orbit
            
    def move(self):
        
        self.x, self.y = self.orbit.nextPos()

class Sprite:
    
    def __init__(self, image_path = DEFAULT_SC_SPRITE, size = (50, 50), thruster_color = (0, 157, 255)):
        
        self.image_path = image_path
        self.size = size
        self.thruster_color = thruster_color
        
        self.image = pygame.image.load(image_path)
        self.sprite = pygame.transform.scale(self.image, self.size)
    
    def transform(self, x, y, theta_degrees):
        
        ''' Return PyGame Image + Rectangle objects for scree.blit onto screen. '''
        
        sc_rot = pygame.transform.rotate(self.sprite, theta_degrees)
        sc_rect = sc_rot.get_rect()
        sc_rect = sc_rect.move((x-sc_rect.centerx, y-sc_rect.centery))
        
        return sc_rot, sc_rect 
    
    def render(self, x,y, theta_degrees, thrust_direction = None):
    
        sc_rot, sc_rect = self.transform(x, y, theta_degrees)
        
        
        

class Spacecraft(Asset):
    
    def __init__(self, name, starting_x = 0.0, starting_y = 0.0, mass = 0.0, gas_level = 0.0, thrust_force = 0.0, sprite_path = None):
        
        super().__init__(name, starting_x, starting_y, mass)
        self.gas_level = gas_level
        self.thrust = False
        self.thrust_direction = '-y' # +/-x,-y
        self.thrust_mag = thrust_force
        self._brakes = False
        self.sprite = sprite_path
    
    def bodyTransform(self, vector):
        
        ''' Body pointing towards self.vel '''
        
        return np.matmul(self.vel.rot_matrix, vector)
    
    def findClosestPlanet(self, planets):
        
        current_distance = self.calcDistance(planets[0])
        index_of_closest = 0
        current_index = 0
        for num in range(len(planets)):
            if self.calcDistance(planets[current_index]) < current_distance: 
                index_of_closest = current_index
                current_distance = self.calcDistance(planets[current_index])
            current_index += 1
        
        return planets[index_of_closest]
    
    def getThrustImpulse(self):
        
        if self.gas_level <= 0.0:
            self.gas_level = 0.0
            self.thrust = False
        
        if self.thrust:
            
            self.gas_level -= self.thrust_mag / 1000
            
            vel_vec = self.vel.vec
            if np.linalg.norm(self.vel.vec) == 0.0:
                vel_vec = [0,-1]                
            
            if self.thrust_direction == '-y':
                # vec = [0,-1]
                vector = vel_vec
            elif self.thrust_direction == '+y':
                # vec = [0,1]
                vector = np.matmul(getRotMatrix(np.pi), vel_vec)
            elif self.thrust_direction == '-x':
                # vec = [1,0]
                vector = np.matmul(getRotMatrix(np.pi/2), vel_vec)
            elif self.thrust_direction == '+x':
                # vec = [-1,0]
                vector = np.matmul(getRotMatrix(np.pi * 1.5), vel_vec)
                
            force = Force(vector[0], vector[1], self.thrust_mag)
            # print(math.degrees(angleBetween(self.vel.vec, [force.x,force.y])))  
            return Momentum.fromImpulse(force, 1/FPS)
        
        return Momentum(0.0, 0.0)
    
    def updateMomentum(self, planets = None):
        
        # Thrust impulse
        thrust_i = self.getThrustImpulse()
        
        # Planet impulse
        planet_i = Momentum(0.0, 0.0)
        if planets:
            closes_planet = self.findClosestPlanet(planets)
            if closes_planet:
                planet_f = self.calcGravitationalForce(closes_planet)
                planet_i = Momentum.fromImpulse(planet_f, 1/FPS) 
        
        # print('Thrust', thrust_i)
        # print('Planet', planet_i)
        self.p = self.p + thrust_i + planet_i       
    
    def move(self):
        
        if not self.brakes:
            delta_time = 1/FPS
            self.x += self.vel.x * delta_time
            self.y += self.vel.y * delta_time
    
    def refresh(self, planets = None):
        
        self.updateMomentum(planets)
        self.move()    
   
    @property
    def brakes(self):
        return self._brakes

    @brakes.setter
    def brakes(self, val):
        self._brakes = val
        self.vel = Velocity(0.0, 0.0)
        self.thrust = False
    
    # def calculateDirectionalVelocity(self, system_momentum_const, current_total_planetary_momentum, closest_planet_impulse, thrust_impulse):

    #     return (system_momentum_const - current_total_planetary_momentum + closest_planet_impulse + thrust_impulse) / self.mass
    
    # def getPos(self, time):
    #     return (self.trajectory.x(time), self.trajectory.y(time))       
        
       
        
