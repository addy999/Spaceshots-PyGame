import pygame
import os, sys
import math
import numpy as np
import time
import ctypes

sys.path.append('./')
from assests import *
from scene import *
from utilities import *

class GameScene(Scenario):
    
    def __init__(self, 
                 resolution,
                 sc,
                 planets,
                 sc_start_pos = None, 
                 win_region = tuple, # ([x1,x2], [y1,y2])
                 win_velocity = 0.0,
                 win_region_color = (0.0, 255, 174),
                 background = None # Image path / color tuple
                ):
        
        super().__init__(resolution, sc, planets, sc_start_pos)
        self.background = background
        self.win_region = win_region
        self.win_min_velocity = win_velocity
        self.win_region_color = win_region_color
        
class Game:
    
    def __init__(self, fullscreen = False, font = 'Helvetica Neue', font_size = 30, fps = 60.0, scenes = []):
        
        pygame.init()
        pygame.font.init()
        
        self.clock = pygame.time.Clock()
        self.fullscreen = fullscreen
        self.fps = fps
        self.font = pygame.font.SysFont(font, font_size)
        self.scenes = scenes
        self.screen = None # current screen
        self.current_scene = self.scenes[0]
        self._bg_loaded = False
    
    def loadImage(self, path, size):
        
        img = pygame.image.load(path)
        img_scaled = pygame.transform.scale(img, size)
        rectangle = img_scaled.get_rect()
        rectangle = rectangle.move((0,0))
        
        return img_scaled, rectangle
    
    def renderBackground(self, scene):
        
        ''' Render background of scene on current game screen '''
              
        if scene.background:
            if (isinstance(scene.background, list) or isinstance(scene.background, tuple)) and len(scene.background) == 3:
                # RGB Value given
                self.screen.fill(scene.background)
            else:
                # Image path given
                if not self._bg_loaded:
                    self._bg_img, self._bg_rect = self.loadImage(scene.background, scene.size)                  
                
                self.screen.blit(self._bg_img, self._bg_rect)   
                  
        else:
            # Default: lack screen
            self.screen.fill((0,0,0))
    
    def renderPlanets(self, scene):
        
        for planet in scene.planets:
            pygame.draw.ellipse(self.screen, planet.color, pygame.Rect(planet.x-25, planet.y-25, 50, 50))
            # Orbit
            pygame.draw.ellipse(self.screen, (255,255,255), pygame.Rect(planet.orbit.center_x-planet.orbit.a, planet.orbit.center_y-planet.orbit.b, planet.orbit.a*2, planet.orbit.b*2), 1)
    
    def renderWinRegion(self, scene):
        
        pygame.draw.line(self.screen, scene.win_region_color, (scene.win_region[0][0], scene.win_region[0][1]), (scene.win_region[1][0], scene.win_region[1][1]), 15)
    
    def createScreen(self, scene = None):
        
        ''' Start screen window '''
        
        if not scene:
            scene = self.current_scene
        
        if self.fullscreen:
            
            # Only windows!
            
            ctypes.windll.user32.SetProcessDPIAware()
            self.screen = pygame.display.set_mode((scene.size[0], scene.size[1]), pygame.FULLSCREEN)
            
        else:
            self.screen = pygame.display.set_mode((scene.size[0], scene.size[1]))
    
    def renderSc(self, scene):
        
        sc_rot = self.current_scene.sc.sprite.sprite
        sc_rect = self.current_scene.sc.sprite.rect
        
        self.screen.blit(sc_rot, sc_rect)
    
    def renderScene(self, scene):
        
        '''
        Render scene onto game screen
        '''
        
        if pygame.display.get_surface().get_size() != scene.size:
            self.createScreen(scene)
            
        # background
        self.renderBackground(scene)
        
        # planets
        self.renderPlanets(scene)
        
        # win region
        self.renderWinRegion(scene)
        
        # spacecraft
        self.renderSc(scene)
        
        # Hu
        self.renderHud(scene)
    
    def renderHud(self, scene):
        
        sc = self.current_scene.sc
        
        # Gas level
        text_surface = self.font.render('Gas: ' + str(sc.gas_level), True, (255,255,255))
        self.screen.blit(text_surface, (scene.size[0]-100, scene.size[1]-60))
        
        # Velocity
        text_surface = self.font.render('Velocity: ' + str(round(sc.vel.mag,2)), True, (255,255,255))
        self.screen.blit( text_surface, (scene.size[0]-145, scene.size[1]-20))
        
        # Escape velocity needed
        text_surface = self.font.render('Velocity Required: ' + str(round(self.current_scene.win_min_velocity, 2)), True, (255,255,255))
        self.screen.blit(text_surface, (0.0, scene.size[1]-20))
    
    def captureSpacecraftControls(self, event):
            
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
            
            self.current_scene.sc.thrust = True
            if event.key == pygame.K_DOWN:
                    self.current_scene.sc.thrust_direction = '+y'
            if event.key == pygame.K_UP:
                    self.current_scene.sc.thrust_direction = '-y'
            if event.key == pygame.K_RIGHT:
                    self.current_scene.sc.thrust_direction = '-x'
            if event.key == pygame.K_LEFT:
                    self.current_scene.sc.thrust_direction = '+x'
        elif event.type == pygame.KEYUP and event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
        
            self.current_scene.sc.thrust = False                
    
    def checkSceneWin(self, scene):
        
        sc = self.current_scene.sc
        win_region_1 = self.current_scene.win_region[0]
        win_region_2 = self.current_scene.win_region[1]
        
        won = False
        failed = False
        
        # Win if
        
        if win_region_1[0] == 0 and win_region_2[0] == 0:
            if sc.x <= 0.0  and win_region_1[1] <= sc.y <= win_region_2[1] and sc.vel.mag >= self.current_scene.win_min_velocity:
                won = True
        elif win_region_1[1] == 0 and win_region_2[1] == 0:
            if sc.y <= 0.0  and win_region_1[0] <= sc.x <= win_region_2[0] and sc.vel.mag >= self.current_scene.win_min_velocity:
                won = True 
        elif win_region_1[0] <= sc.x <= win_region_2[0]  and win_region_1[1] <= sc.y <= win_region_2[1] and sc.vel.mag >= self.current_scene.win_min_velocity:
            won = True
                
        # Out of bounds
        if not 0.0 < sc.x < self.current_scene.size[0] or not 0.0 < sc.y < self.current_scene.size[1]:
            failed = True
        
        return won, failed
    
    def renderFullscreenDialog(self, text, xoffset = 0, yoffset = 0):
        
        screen_x = self.current_scene.size[0]
        screen_y = self.current_scene.size[1]
        
        text_surface = self.font.render(text, True, (255,255,255))
        self.screen.fill((0, 0, 0))
        self.screen.blit( text_surface, (screen_x/2 + xoffset, screen_y/2 + yoffset)) 
        pygame.display.update()
        
        time.sleep(1.5)
        
    def nextScene(self, done):
        
        current_i = self.scenes.index(self.current_scene)
        
        if current_i < len(self.scenes) - 1:
            self.current_scene  = self.scenes[current_i+1]
            return self.scenes[current_i+1], done
        else:
            return self.current_scene, True
    
    def renderFinalMessage(self, won, failed):
        
        center_x = self.current_scene.size[0] / 2
        
        if won:
            
            self.renderFullscreenDialog('You\'re a gravity assist pro :D', xoffset= center_x -  400)
        
        else:
            
            self.renderFullscreenDialog('No worries, see ya next time!', xoffset = center_x - 425)
    
    def startGame(self, scene_to_start_at = None):
        
        self.createScreen(scene_to_start_at)
        dt = 1 / self.fps
        
        done = False        
        while not done:
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        done = True
                    
                # Modify spacecraft thrusters 
                self.captureSpacecraftControls(event)
                        
            # Iterate next planetary + sc positions
            self.current_scene.updateAllPos(dt)
                
            # Check exit conditions
            won, failed = self.checkSceneWin(self.current_scene)
            if won:
                self.renderFullscreenDialog('Won!', xoffset=-10)
                self.current_scene, done = self.nextScene(done)
            elif failed:
                self.renderFullscreenDialog('Oops, try again!', xoffset=-75)
                self.current_scene.resetPos()
            
            if won or failed: self._bg_img, self._bg_rect = None, None
            
            if not done:
                # Draw modified scene            
                self.renderScene(self.current_scene)
                pygame.display.update()
                dt = self.clock.tick(self.fps) / 1000

        self.renderFinalMessage(won, failed)
        pygame.quit()
        
          
        