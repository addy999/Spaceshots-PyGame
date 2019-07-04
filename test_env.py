import pygame
import os, sys
import math
sys.path.append('./astron')
from assests import *

pygame.init()

# Setup screen
screen_x, screen_y = 500, 500
screen = pygame.display.set_mode((screen_x, screen_y))

# Utilities 
done = False
clock = pygame.time.Clock()

# Assets
sc = Spacecraft('Test', 225, 450, 100, thrust_force = 3000, gas_level = 1000)

while not done:
        
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
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
                              
        sc_sprite = sc.sprite.sprite
        sc_rot = pygame.transform.rotate(sc_sprite, math.degrees(sc.vel.getTheta())-90)
        sc_rect = sc_rot.get_rect()
        sc_rect = sc_rect.move((sc.x-sc_rect.centerx, sc.y-sc_rect.centery))
        screen.blit(sc_rot, sc_rect)
        
        print(sc.thrust_direction)
        
        pygame.display.update()
        clock.tick(FPS)