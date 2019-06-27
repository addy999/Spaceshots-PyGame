from .utilities import *

class Asset:
    
    def __init__(self, name, x = 0.0, y = 0.0, mass = 0, x_Vel = 0.0, y_vel = 0.0):
        
        self.x = x
        self.y = y
        self.name = name
        self.mass = mass
        self.x_vel = x_Vel
        self.y_vel = y_vel
        self._p = Momentum(self.x_vel, self.y_vel, self.mass)
    
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
        self.x_vel = val.x / self.mass
        self.y_vel = val.y / self.mass
     
           
class Planet(Asset):
    
    def __init__(self, name, x  = 0.0, y = 0.0, mass = 0.0, orbit = Orbit, orbit_period = 30.0):
    
        super().__init__(name, x, y, mass)
        self.g = 6.67408e-11 # m^3/kg*s^2
        self.orbit = orbit
        self.orbit_period = orbit_period
        self.angular_step = self.__getAngularStep()
    
    def __getAngularStep(self):
        
        return 2*np.pi / (self.orbit_period * FPS)
            
    def move(self):
        
        self.x, self.y = self.orbit.nextPos(self.angular_step)

class Spacecraft(Asset):
    
    def __init__(self, name, starting_x = 0.0, starting_y = 0.0, mass = 0.0, gas_level = 0.0, thrust_force = 0.0):
        
        super().__init__(name, starting_x, starting_y, mass)
        self.gas_level = gas_level
        self.thrust = False
        self.thrust_direction = '-y' # +/-x,-y
        self.thrust_mag = thrust_force
    
    def findClosestPlanet(self, planets):
        
        current_distance = calcDistance(planets[0].x, planets[0].y, self.x, self.y)
        index_of_closest = 0
        current_index = 0
        for num in range(len(planets)):
            current_index += 1
            if(calcDistance(planets[current_index].x, planets[current_index].y, self.x, self.y) < current_distance): 
                index_of_closest = current_index
                current_distance = calcDistance(planets[current_index].x, planets[current_index].y, self.x, self.y)
        
        if current_distance < PLANET_DISTANCE_THRESHOLD:
            return planets[index_of_closest]
        else:
            return None
    
    def getThrustImpulse(self):
        
        if self.thrust:
            if self.thrust_direction == '-y':
                force = Force(0.0, 1.0, self.thrust_mag)
                return Momentum.fromImpulse(force, 1/FPS)
            elif self.thrust_direction == '-x':
                force = Force(1.0, 0.0, self.thrust_mag)
                return Momentum.fromImpulse(force, 1/FPS)
            elif self.thrust_direction == '+x':
                force = Force(-1.0, 0.0, self.thrust_mag)
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
        
        self.p = self.p + thrust_i + planet_i       
                
    
    def calculateDirectionalVelocity(self, system_momentum_const, current_total_planetary_momentum, closest_planet_impulse, thrust_impulse):

        return (system_momentum_const - current_total_planetary_momentum + closest_planet_impulse + thrust_impulse) / self.mass
    
    # def getPos(self, time):
    #     return (self.trajectory.x(time), self.trajectory.y(time))       
        
        
        
