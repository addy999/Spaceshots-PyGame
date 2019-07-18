import sys, os
import numpy as np
import pygame
import math
modpath = os.path.abspath(os.path.split(sys.argv[0])[0])
sys.path.append(modpath)

from .utilities import *

DEFAULT_SC_SPRITE = getModpath() + r'\images\ship1.png'

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
    
    def __init__(self, name, mass = 0.0, orbit = Orbit, color = (100,100,100)):
    
        super().__init__(name, 0.0, 0.0, mass)
        self.g = 6.67408e-11 # m^3/kg*s^2
        self.orbit = orbit
        self.color = color
        self.move()
            
    def move(self, dt = 1.0):
        
        self.x, self.y = self.orbit.nextPos(dt)

class Sprite:
    
    def __init__(self, image_path = DEFAULT_SC_SPRITE, size = (100, 100), theta_deg_offset = 90.0):
    
        self.size = size
        self.image_path = image_path
        self.theta_deg_offset = theta_deg_offset
        
        self.checkPath(image_path)
        self._loadAllImages(image_path)
        
    def checkPath(self, image_path):
        
        if image_path[-3:] != 'png':
            raise ValueError('Must be a PNG image.')
        
    def _loadAllImages(self, image_path):
        
        self.base = pygame.image.load(image_path)
        self.px = pygame.image.load(image_path[:-4] + '_+x' + '.png')
        self.py = pygame.image.load(image_path[:-4] + '_+y' + '.png')
        self.nx = pygame.image.load(image_path[:-4] + '_-x' + '.png')
        self.ny = pygame.image.load(image_path[:-4] + '_-y' + '.png')
    
    def transform(self, x, y, radians, thruster_direction = None):
        
        ''' Return PyGame Image + Rectangle objects for scree.blit onto screen. '''
        
        img = self.loadThrusterImage(thruster_direction)
        sc_rot = pygame.transform.rotate(img, math.degrees(radians) + self.theta_deg_offset)
        sc_rect = sc_rot.get_rect()
        sc_rect = sc_rect.move((x-sc_rect.centerx, y-sc_rect.centery))
        
        self.sprite = sc_rot
        self.rect = sc_rect 
        
        return sc_rot, sc_rect
    
    def loadThrusterImage(self, thrust_direction = None):
        
        if thrust_direction:
            if thrust_direction=='+x':
                img = pygame.transform.scale(self.px, self.size)
            if thrust_direction=='+y':
                img = pygame.transform.scale(self.py, self.size)
            if thrust_direction=='-x':
                img = pygame.transform.scale(self.nx, self.size)
            if thrust_direction=='-y':
                img = pygame.transform.scale(self.ny, self.size)
        
        else:
            img = pygame.transform.scale(self.base, self.size)
        
        return img
    
    # def _render(self, x,y, theta_degrees, thrust_direction = None):
    
    #     sc_rot, sc_rect = self.transform(x, y, theta_degrees)
        
class Spacecraft(Asset):
    
    def __init__(self, name, mass = 0.0, gas_level = 0.0, thrust_force = 0.0, sprite = None):
        
        super().__init__(name, 0.0, 0.0, mass)
        self.gas_level = gas_level
        self._initial_gas_level = gas_level
        self.thrust = False
        self.thrust_direction = '-y' # +/-x,-y
        self.thrust_mag = thrust_force
        self.sprite = sprite
        
        # Load default if none given
        if not sprite:
            self.sprite = Sprite()
    
    def bodyTransform(self, vector):
        
        ''' Body pointing towards self.vel '''
        
        return np.matmul(self.vel.rot_matrix, vector)
       
    def getThrustImpulse(self, time):
        
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
            return Momentum.fromImpulse(force, time)
        
        return Momentum(0.0, 0.0)
    
    def setNetMomentum(self, impulse_time, external_force = None):
        
        # Thrust impulse
        thrust_i = self.getThrustImpulse(impulse_time)
        
        # External impulse
        if external_force:
            external_i = Momentum.fromImpulse(external_force, impulse_time) 
        else:
            external_i = Momentum(0.0, 0.0)
        
        self.p = self.p + thrust_i + external_i       
    
    def move(self, time):
        
        self.x += self.vel.x * time
        self.y += self.vel.y * time
    
    def reset(self, sc_start_pos = None):
        
        self.thrust = False
        if sc_start_pos:
            self.x, self.y = sc_start_pos
        self.p = Momentum(0.0, 0.0)
        self.gas_level = self._initial_gas_level
               
    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, val):
        self._p = val
        self.vel = Velocity(val.x / self.mass, val.y / self.mass)
        if self.thrust:
            self.sprite.transform(self.x, self.y, self.vel.theta, self.thrust_direction)
        else:
            self.sprite.transform(self.x, self.y, self.vel.theta)     
        
        # print(val)   
       
        
