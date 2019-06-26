class Asset:
    
    def __init__(self, name, x = 0.0, y = 0.0, mass = 0):
        
        self.x = x
        self.y = y
        self.name = name
        self.mass = mass
    
    def resetPos(self):
        
        self.x = 0
        self.y = 0
           
class Spacecraft(Asset):
    
    def __init__(self, name, starting_x = 0.0, starting_y = 0.0, mass = 0.0, gas_level = 0.0):
        
        super().__init__(name, starting_x, starting_y, mass)
        self.gas_level = gas_level
        self.thrust = False
        self.thrust_direction = '-y' # +/-x,-y
        
    # def getPos(self, time):
    #     return (self.trajectory.x(time), self.trajectory.y(time))

class Planet(Asset):
    
    def __init__(self, name, x  = 0.0, y = 0.0, mass = 0.0, trajectory = None):
    
        super().__init__(name, x, y, mass)
        self.g = 6.67408e-11 # m^3/kg*s^2
        self.trajectory = trajectory

        
        
        
        
