import pygame
import os, sys
import math
sys.path.append('./')
from assests import *
from utilities import *

pygame.init()
pygame.font.init()

# Setup screen
screen_x, screen_y = 500, 500
screen = pygame.display.set_mode((screen_x, screen_y))
font = pygame.font.SysFont('Helvetica Neue', 30)
win_region_x = (0.0, 0.0)
win_region_y = (0.0, 100.0)
won = False
min_speed = 190.0

# background
stars = pygame.image.load(r'C:\Users\addym\Documents\Gravity Assists\astron\images\stars_1.jpg')
stars_scaled = pygame.transform.scale(stars, (screen_x, screen_y))
rect = stars_scaled.get_rect()
rect = rect.move((0,0))
screen.fill((0, 0, 0))
# screen.blit(stars_scaled, (0,0))
screen.blit(stars_scaled, rect)

# sc
sc_sprite= pygame.image.load(r'C:\Users\addym\Documents\Gravity Assists\astron\images\ship1.png')
sc_sprite = pygame.transform.scale(sc_sprite, (50,50))

# Utilities 
done = False
clock = pygame.time.Clock()
color = (0, 128, 255)

# Assets
sc = Spacecraft('Test', 225, 450, 100, thrust_force = 3000, gas_level = 1000)
orbit = Orbit(100, 300, 0, screen_y, CW=False, orbit_period = 100.0, progress = -np.pi/8)
orbit2 = Orbit(100, 300, screen_x, screen_y/2, CW=True, orbit_period = 80.0, progress = np.pi*0.8)
planet = Planet('Test', mass = 1e16, orbit = orbit)
planet2 = Planet('Test2', mass = 2e16, orbit = orbit2)

orbit3 = Orbit(300, 100, screen_x*0.75, screen_y*0.3, CW=True, orbit_period = 80.0, progress = np.pi/2)
planet3 = Planet('Test', mass = 2e16, orbit = orbit3)

planets = [planet3]

while not done:
        
        # screen.fill((0, 0, 0))
        # screen.blit(stars, (0,0))
        screen.blit(stars_scaled, rect)
        
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
        pygame.draw.line(screen, (0.0, 255, 174), (0.0, win_region_y[0]), (0.0, win_region_y[1]), 15)
        
        # Planet
        for planet in planets:
                planet.move()
                pygame.draw.ellipse(screen, (100,100,100), pygame.Rect(planet.x-25, planet.y-25, 50, 50))
                # Orbit
                pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(planet.orbit.center_x-planet.orbit.a, planet.orbit.center_y-planet.orbit.b, planet.orbit.a*2, planet.orbit.b*2), 1)
        
        # Update spacecraft positions 
        sc.refresh(planets)
        vel_matrix = sc.vel.rot_matrix
        tip = [sc.x, sc.y]
        a = np.matmul(vel_matrix, [sc.x-25,sc.y+35])
        b = np.matmul(vel_matrix, [sc.x+25,sc.y+35])
        
        # pygame.draw.polygon(screen, color, [
        #         tip,
        #         a,
        #         b,
        #         ])
        # print(sc.vel, sc.vel.getTheta())
        # print(sc.vel.vec - sc.bodyTransform(sc.vel.vec))
        # if sc.thrust:
        #         if sc.thrust_direction == '+y':
        #                 pygame.draw.polygon(screen, (255, 100, 0), [
        #                         tip,
        #                         tip+np.matmul([-5,-10], vel_matrix),
        #                         tip+np.matmul([5,-10], vel_matrix),
        #                         ])
        #         if sc.thrust_direction == '-y':
        #                 pygame.draw.polygon(screen, (255, 100, 0), [
        #                         tip+np.matmul([0,45], vel_matrix),
        #                         tip+np.matmul([-5, 55], vel_matrix),
        #                         tip+np.matmul([5, 55], vel_matrix),
        #                         ])
        #         if sc.thrust_direction == '-x':
        #                 pygame.draw.polygon(screen, (255, 100, 0), [
        #                         [sc.x, sc.y]+np.matmul([-10,35/2], vel_matrix),
        #                         [sc.x, sc.y]+np.matmul([-20, 35/2-5], vel_matrix),
        #                         [sc.x, sc.y]+np.matmul([-20, 35/2+5], vel_matrix),
        #                         ])
        #         if sc.thrust_direction == '+x':
        #                 pygame.draw.polygon(screen, (255, 100, 0), [
        #                         [sc.x, sc.y]+np.matmul([10,35/2], vel_matrix),
        #                         [sc.x, sc.y]+np.matmul([20,35/2-5], vel_matrix),
        #                         [sc.x, sc.y]+np.matmul([20,35/2+5], vel_matrix),
        #                         ])
        vel = 50 * unit_vector((sc.vel.x, sc.vel.y))
        # pygame.draw.line(screen, (0.0, 255, 174), tip, tip+vel, 2)
        # pygame.draw.line(screen, (255,255,255), tip, tip-vel, 15)
        
        sc_rot = pygame.transform.rotate(sc_sprite, math.degrees(sc.vel.getTheta())+90)
        sc_rect = sc_rot.get_rect()
        sc_rect = sc_rect.move((sc.x-sc_rect.centerx, sc.y-sc_rect.centery))
        screen.blit(sc_rot, sc_rect)
        
                 
        # Update screen
        text_surface = font.render('Gas: ' + str(sc.gas_level), True, (255,255,255))
        screen.blit( text_surface, (screen_x-100, screen_y-60))
        text_surface = font.render('Velocity: ' + str(round(sc.vel.mag,2)), True, (255,255,255))
        screen.blit( text_surface, (screen_x-145, screen_y-20))
        
        pygame.display.update()
        clock.tick(FPS)
        
        # check if won or lost
        # Won
        if sc.x<0.0 and win_region_y[0] <= sc.y <= win_region_y[1] and sc.vel.mag >= min_speed:
                won = True
                done = True
        # Out of bounds
        elif not 0.0 < sc.x < screen_x or not 0.0 < sc.y < screen_y:
                done = True

if won: 
        text_surface = font.render('Won!', True, (255,255,255))
else:
        text_surface = font.render('Lost :(', True, (255,255,255))
         
done = False
while not done:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        done = True
                        
        screen.fill((0, 0, 0))
        screen.blit( text_surface, (screen_x/2, screen_y/2)) 
        pygame.display.update()
        clock.tick(FPS)
        
# pygame.quit()
