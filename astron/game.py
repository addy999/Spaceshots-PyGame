import pygame
import os, sys
import math
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
                 initial_orbit_progress = None,
                 win_region = tuple, # ([x1,x2], [y1,y2])
                 win_velocity = None,
                 win_region_color = (0.0, 255, 174),
                 background = None # Image path / color tuple
                ):
        
        super().__init__(resolution, sc, planets, sc_start_pos, initial_orbit_progress)
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
        self.scenes = scenes
        self.screen = None # current screen
        self.current_scene = self.scenes[0]
    
    def renderBackground(self, scene):
        
        ''' Render background of scene on current game screen '''
        
        if scene.background:
            if isinstance(scene.background, list) and list(scene.background) == 3:
                # RGB Value
                self.screen.fill(scene.background)
            else:
                # Image path
                img = pygame.image.load(scene.background)
                img_scaled = pygame.transform.scale(img, scene.size)
                rectangle = img_scaled.get_rect()
                rectangle = rectangle.move((0,0))
                self.screen.blit(img_scaled, rectangle)
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
            self.screen = pygame.display.set_mode((scene.size[0], scene.size[1]), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((scene.size[0], scene.size[1]))
    
    def renderScene(self, scene):
        
        '''
        Render scene onto game screen
        '''
        
        if pygame.display.get_surface().get_size() != scene.size:
            print(pygame.display.get_surface().get_size())
            self.createScreen(scene)
            
        # background
        self.renderBackground(scene)
        
        # planets
        self.renderPlanets(scene)
        
        # win region
        self.renderWinRegion(scene)
        
        # spacecraft
        
    
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
      
    def startGame(self, scene_to_start_at = None):
        
        self.createScreen(scene_to_start_at)
        refresh_rate = 1 / self.fps
        
        done = False        
        while not done:
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        done = True
                    
                # Modify spacecraft thrusters 
                self.captureSpacecraftControls(event)
                        
            # Iterate next planetary + sc positions
            self.current_scene.updateAllPos(refresh_rate)
                
            # Draw modified scene            
            self.renderScene(self.current_scene)
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        
          
        