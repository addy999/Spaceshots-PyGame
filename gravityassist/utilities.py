import numpy as np

class Velocity:
    
    def __init__(self, x_vel, y_vel):
        
        self.x = x_vel
        self.y = y_vel
    
    def getMag(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
class Orbit:
    
    def __init__(self, a, b, center_x, center_y, angular_step = 0.017, progress = 0.0):
        self.a = a
        self.b = b
        self.center_x = center_x
        self.center_y = center_y
        self.angular_step = angular_step
        self.progress = progress
        
    def x(self, progress):
        return self.a * np.cos(progress) + self.center_x
    
    def y(self, progress):
        return self.b * np.sin(progress) + self.center_y
    
    def nextPos(self):
        self.progress += self.angular_step
        return self.x(self.progress), self.y(self.progress)
        
