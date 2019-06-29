import numpy as np
import math

############### Constants ###############

FPS = 60 
PLANET_DISTANCE_THRESHOLD = 100000

########################################

class Velocity:
    
    def __init__(self, x_vel, y_vel):
        
        self.x = x_vel
        self.y = y_vel
    
    def getMag(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        
        return str((self.x, self.y))

class Force:
    
    def __init__(self, x_vector, y_vector, mag):
        
        hyp = (x_vector ** 2 + y_vector ** 2) ** 0.5
        ratio = mag / hyp
        self.x = x_vector * ratio
        self.y = y_vector * ratio
        self.mag = mag  
    
    def __repr__(self):  
         
        return str((self.x, self.y))      

class Momentum:
    
    def __init__(self, x_vel, y_vel, mass = 1):
        
        self.x = mass * x_vel
        self.y = mass * y_vel
    
    @classmethod
    def fromImpulse(cls, force = Force, duration = float):
        
        x = force.x * duration
        y = force.y * duration
        
        return cls(x, y)

    def __add__(self, new):
        
        self.x += new.x
        self.y += new.y
        
        return self 

    def __repr__(self):
        
        return str((self.x, self.y))
    
class Orbit:
    
    def __init__(self, a, b, center_x, center_y, progress = 0.0, CW = True, orbit_period = 30.0):
        self.a = a
        self.b = b
        self.center_x = center_x
        self.center_y = center_y
        self.progress = progress
        self.cw = CW
        self.orbit_period = orbit_period
        self.angular_step = self.__getAngularStep()
        
    def x(self, progress):
        return self.a * np.cos(progress) + self.center_x
    
    def y(self, progress):
        return self.b * np.sin(progress) + self.center_y
    
    def __getAngularStep(self):
        return 2*np.pi / (self.orbit_period * FPS)
    
    def nextPos(self):
        if self.cw:
            self.progress += self.angular_step
        else:
            self.progress -= self.angular_step
            
        return self.x(self.progress), self.y(self.progress)

    def resetPos(self):
        self.progress = 0
        return self.x(self.progress), self.y(self.progress)
        
