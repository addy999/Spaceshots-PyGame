import pygame
import sys
sys.path.append('./')
from assests import *
from utilities import *

pygame.init()
pygame.font.init()

# Setup screen
screen_x, screen_y = 500, 500
screen = pygame.display.set_mode((screen_x, screen_y))
screen.fill((0, 0, 0))
font = pygame.font.SysFont('Helvetica Neue', 30)
win_region_x = (screen_x/2-50, screen_x/2+50)
won = False

# Utilities 
done = False
clock = pygame.time.Clock()
color = (0, 128, 255)

# Assets
sc = Spacecraft('Test', 225, 450, 100, thrust_force = 3000, gas_level = 3500)
orbit = Orbit(100, 300, 0, screen_y, CW=False, orbit_period = 100.0, progress = -np.pi/8)
orbit2 = Orbit(100, 300, screen_x, screen_y/2, CW=True, orbit_period = 80.0, progress = np.pi*0.8)
planet = Planet('Test', mass = 1e16, orbit = orbit)
planet2 = Planet('Test2', mass = 2e16, orbit = orbit2)
planets = [planet, planet2]

while not done:
        
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        sc.brakes = not sc.brakes
                        # print(sc.vel)
                elif event.type == pygame.KEYDOWN and event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                        sc.thrust = True
                        if event.key == pygame.K_DOWN:
                                sc.thrust_direction = '+y'
                        if event.key == pygame.K_UP:
                                sc.thrust_direction = '-y'
                        if event.key == pygame.K_RIGHT:
                                sc.thrust_direction = '-x'
                        if event.key == pygame.K_LEFT:
                                sc.thrust_direction = '+x'
                elif event.type == pygame.KEYUP and event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                        sc.thrust = False
               
        # Goal post
        pygame.draw.line(screen, (0.0, 255, 174), (win_region_x[0], 0.0), (win_region_x[1], 0.0), 15)
        
        # Planet
        for planet in planets:
                planet.move()
                pygame.draw.ellipse(screen, (100,100,100), pygame.Rect(planet.x-25, planet.y-25, 50, 50))
                # Orbit
                pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(planet.orbit.center_x-planet.orbit.a, planet.orbit.center_y-planet.orbit.b, planet.orbit.a*2, planet.orbit.b*2), 1)
        
        # Update spacecraft positions 
        sc.refresh(planets)
        pygame.draw.polygon(screen, color, [
                [sc.x, sc.y],
                [sc.x-25, sc.y+35],
                [sc.x+25, sc.y+35],
                ])
        if sc.thrust:
                if sc.thrust_direction == '+y':
                        pygame.draw.polygon(screen, (255, 100, 0), [
                                [sc.x, sc.y],
                                [sc.x-5, sc.y-10],
                                [sc.x+5, sc.y-10],
                                ])
                if sc.thrust_direction == '-y':
                        pygame.draw.polygon(screen, (255, 100, 0), [
                                [sc.x, sc.y+35],
                                [sc.x-5, sc.y+35+10],
                                [sc.x+5, sc.y+35+10],
                                ])
                if sc.thrust_direction == '-x':
                        pygame.draw.polygon(screen, (255, 100, 0), [
                                [sc.x-10, sc.y+35/2],
                                [sc.x-20, sc.y+35/2-5],
                                [sc.x-20, sc.y+35/2+5],
                                ])
                if sc.thrust_direction == '+x':
                        pygame.draw.polygon(screen, (255, 100, 0), [
                                [sc.x+10, sc.y+35/2],
                                [sc.x+20, sc.y+35/2-5],
                                [sc.x+20, sc.y+35/2+5],
                                ])
                 
        # Update screen
        # print(sc.vel, sc.x, sc.y)
        if not won:
                text_surface = font.render(str(sc.gas_level), True, (255,255,255))
                screen.blit( text_surface, (screen_x-50, screen_y-20))
        else:
                text_surface = font.render('Won!', True, (255,255,255))
                screen.blit( text_surface, (screen_x-50, screen_y-20))
                done = True
        
        
        pygame.display.update()
        clock.tick(FPS)
        
        # check if won or lost
        # Won
        if win_region_x[0] <= sc.x <= win_region_x[1] and sc.y < 0.0:
                won = True
        # Out of bounds
        elif not 0.0 < sc.x < screen_x or not 0.0 < sc.y < screen_y:
                done = True

if won: 
        print('Won!')      
else:
        print('Loser')
        
pygame.quit()
