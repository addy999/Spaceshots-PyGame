import pygame
import os, sys
import math
import numpy as np
import time
import ctypes

modpath = os.path.abspath(os.path.split(sys.argv[0])[0])
sys.path.append(modpath)

from .assests import *
from .scene import *
from .utilities import *

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
        self._attempts = 0
        self._won = False
        
class Game:
    
    def __init__(self, fullscreen = False, font = 'Helvetica Neue', font_size = 30, fps = 60.0, scenes = []):
        
        pygame.init()
        pygame.font.init()
        
        self.clock = pygame.time.Clock()
        self.fullscreen = fullscreen
        self.fps = fps
        self.last_dt = 1 / fps
        self.current_dt = 1 / fps
        self.font = pygame.font.SysFont(font, font_size)
        self.scenes = scenes
        self.screen = None # current screen
        self.extra_time = 0.0
        self.current_scene = self.scenes[0]
        self._bg_loaded = False
        self.__rpk = 45 / 4e16 # radius per kilogram of planet
        self._done = False        
        
        for scene in self.scenes:
            scene._attempts = 0
            scene._won = False
    
    def wait(self, time_in_seconds):
        
        time.sleep(time_in_seconds)
        self.extra_time = time_in_seconds    
    
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
        
        rpk = self.__rpk
        
        for planet in scene.planets:
            
            pygame.draw.ellipse(self.screen, planet.color, pygame.Rect(planet.x-rpk*planet.mass, planet.y-rpk*planet.mass, rpk*planet.mass * 2, rpk*planet.mass * 2))
            # Orbit
            pygame.draw.ellipse(self.screen, (255,255,255), pygame.Rect(planet.orbit.center_x-planet.orbit.a, planet.orbit.center_y-planet.orbit.b, planet.orbit.a*2, planet.orbit.b*2), 1)
    
    def renderWinRegion(self, scene):
        
        pygame.draw.line(self.screen, scene.win_region_color, (scene.win_region[0][0], scene.win_region[0][1]), (scene.win_region[1][0], scene.win_region[1][1]), 25)
    
    def createScreen(self, scene = None):
        
        ''' Start screen window '''
        
        if not scene:
            scene = self.current_scene
        
        if self.fullscreen:
            
            infoObject = pygame.display.Info()
            screen_x, screen_y = infoObject.current_w, infoObject.current_h
            
            if scene.size[0] == screen_x or scene.size[1] == screen_y:
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
        
        # if pygame.display.get_surface().get_size() != scene.size:
        #     self.createScreen(scene)
            
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
        self.screen.blit(text_surface, (scene.size[0]-110, scene.size[1]-60))
        
        # Velocity
        text_surface = self.font.render('Velocity: ' + str(round(sc.vel.mag,2)), True, (255,255,255))
        self.screen.blit( text_surface, (scene.size[0]-145, scene.size[1]-20))
        
        # Escape velocity needed
        text_surface = self.font.render('Velocity Required: ' + str(round(self.current_scene.win_min_velocity, 2)), True, (255,255,255))
        self.screen.blit(text_surface, (0.0, scene.size[1]-20))
        
        # Attempts
        text_surface = self.font.render('Attempts: ' + str(self.current_scene._attempts), True, (255,255,255))
        self.screen.blit(text_surface, (scene.size[0]-150, 10.0))
        
        # Level counter
        text_surface = self.font.render('Level ' + str(self.scenes.index(self.current_scene)+1), True, (255,255,255))
        self.screen.blit(text_surface, (scene.size[0]-150, 30))
    
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
        screen_x = self.current_scene.size[0]
        screen_y = self.current_scene.size[0]
        win_region_1 = self.current_scene.win_region[0]
        win_region_2 = self.current_scene.win_region[1]
        
        won = False
        failed = False
        
        # Win if
        
        # vertical
        if win_region_1[0] == win_region_2[0] and win_region_1[0] == 0.0:
            # left half
            if sc.x <= 0 and win_region_1[1] <= sc.y <= win_region_2[1] and sc.vel.mag >= self.current_scene.win_min_velocity:
                won = True
        elif win_region_1[0] == win_region_2[0] and win_region_1[0] == screen_x:
            # right half
            if sc.x >= screen_x and win_region_1[1] <= sc.y <= win_region_2[1] and sc.vel.mag >= self.current_scene.win_min_velocity:
                won = True
        # Horizontal
        if win_region_1[1] == win_region_2[1] and win_region_1[1] == 0.0:
            # top half
            if sc.y <= 0 and win_region_1[0] <= sc.x <= win_region_2[0] and sc.vel.mag >= self.current_scene.win_min_velocity:
                won = True
        elif win_region_1[1] == win_region_2[1] and win_region_1[1] == screen_y:
            # bottom half
            if sc.y >= screen_y and win_region_1[0] <= sc.x <= win_region_2[0] and sc.vel.mag >= self.current_scene.win_min_velocity:
                won = True
                
        # Out of bounds
        if not won and (not 0.0 < sc.x < self.current_scene.size[0] or not 0.0 < sc.y < self.current_scene.size[1]):
            failed = True
        
        # Collisions
        for planet in self.current_scene.planets:
            planet_r = self.__rpk*planet.mass
            if planet.x - planet_r <= sc.x <= planet.x + planet_r and planet.y - planet_r <= sc.y <= planet.y + planet_r:
                failed = True
        
        return won, failed
    
    def renderFullscreenDialog(self, texts, xoffsets = [], yoffsets = [], sleep_time = 1.5):
        
        screen_x = self.current_scene.size[0]
        screen_y = self.current_scene.size[1]
        self.screen.fill((0, 0, 0))
        c = 0
        
        if not xoffsets:
            [xoffsets.append(0) for i in range(len(texts))]
        if not yoffsets:
            [yoffsets.append(0) for i in range(len(texts))]
        
        for text in texts:
            text_surface = self.font.render(text, True, (255,255,255))
            self.screen.blit( text_surface, (screen_x/2 + xoffsets[c], screen_y/2 + yoffsets[c])) 
            c+=1 
            
        pygame.display.update()
        
        self.wait(sleep_time)
    
    def playAudio(self, path):
        
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(0)   

    def stopAudio(self):
        
        pygame.mixer.music.stop()  
    
    def nextScene(self):
        
        current_i = self.scenes.index(self.current_scene)
        
        if current_i < len(self.scenes) - 1:
            self.current_scene  = self.scenes[current_i+1]
            return self.scenes[current_i+1]
        else:
            self._done = True
            return self.current_scene
    
    def gameWon(self):
        
        center_x = self.current_scene.size[0] / 2
            
        self.playAudio(getModpath() + r'\music\christmas.mp3')
        self.renderFullscreenDialog([
            'You\'re a gravity assist pro :D',
            'Final score: ' + str(self.calcScore())
            ], 
            xoffsets = [-100, -50.0], yoffsets = [0, 100], sleep_time = 5.0)
        self.stopAudio()  
        
    def gameFail(self):
        
        self.playAudio(getModpath() + r'\music\Cut_kazoo_full.mp3')
        center_x = self.current_scene.size[0] / 2 
        self.renderFullscreenDialog([
            'No worries, see ya next time!', 
            'Final score: ' + str(self.calcScore())], 
            xoffsets = [-100, -50.0], yoffsets = [0, 100],  sleep_time = 5.0)
        self.stopAudio()  
        
    def sceneWin(self):
        
        self.playAudio(getModpath() + r'\music\yeet_vine.mp3')        
        self.renderFullscreenDialog(['Won!'], xoffsets=[-10], sleep_time = 3.5)
        self.current_scene = self.nextScene() #iterate next scene
        self.current_scene.resetPos()
        self.current_scene._attempts += 1
        self.current_scene.won = True    
        self.stopAudio()           
    
    def sceneFail(self):
        
        self.playAudio(getModpath() + r'\music\gottem_vine_cut.mp3')        
        self.renderFullscreenDialog(['Oops, try again!'], xoffsets=[-75], sleep_time = 3.5)
        self.current_scene.resetPos()
        self.current_scene._attempts += 1
        self.stopAudio()   
    
    def calcScore(self):
        
        per_scene_score = 100.0
        attempt_deductions = 10.0
        
        total = 0.0
        
        for scene in self.scenes:
            if scene._won:
                total += per_scene_score 
                if scene._attempts > 1:
                    total -= (scene._attempts-1) * attempt_deductions
            
        if total < 0:
            total = 0.0
            
        return total            
    
    def startGame(self, scene_to_start_at = None, splash = True):
        
        self.createScreen(scene_to_start_at)
        # time.sleep(0.5)
        
        if splash:
            self.renderFullscreenDialog([
                'ASTRON', 
                'Use arrow keys to get to the green region with the required velocity!'
                                        
            ], xoffsets = [-50, -300.0], yoffsets = [0, 100], sleep_time= 5)

        self._done = False        
        while not self._done:
            
            # check game exit conditions
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self._done = True
                    
                # Modify spacecraft thrusters 
                self.captureSpacecraftControls(event)
                        
            # Iterate next planetary + sc positions
            self.current_scene.updateAllPos(self.current_dt)
                
            # Check scene exit conditions
            won, failed = self.checkSceneWin(self.current_scene)
            if won: self.sceneWin()
            elif failed: self.sceneFail()
    
            if not self._done:
                # Draw modified scene            
                self.renderScene(self.current_scene)
                pygame.display.update()
                self.last_dt = self.current_dt
                self.current_dt = self.clock.tick(self.fps) / 1000 # to seconds
                if self.extra_time > 0.0 :
                    self.current_dt -= self.extra_time
                    self.extra_time = 0.0
        
                # print(self.last_dt, self.current_dt)

        if won:
            self.gameWon()
        else:
            self.gameFail()
        
        pygame.quit()
        
          
        