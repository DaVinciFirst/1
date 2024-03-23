import pygame
import os

class Settings():
    def __init__(self):
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        #self.bg_color = (4, 3, 27)
        self.alien_width = self.screen_width // 22
        self.alien_height = self.screen_height // 15
        self.fleet_drop_speed = 15
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.path_to_img = os.path.join(os.path.dirname(__file__), "images")
        self.ship_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 10
        self.score_scale = 1.5
        self.menu_button_width = int(self.screen_width / 6.83)
        self.menu_button_height = int(self.screen_height / 15.36)

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 4
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 1.5
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)