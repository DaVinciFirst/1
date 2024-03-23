import pygame
import os

class Ship():
    def __init__(self, aw_settings, screen):
        self.aw_settings = aw_settings
        self.screen = screen
        self.image = pygame.image.load(aw_settings.path_to_img + os.sep + "ship.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.aw_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.aw_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.aw_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.aw_settings.alien_height * 8:
            self.y -= self.aw_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.y = self.y

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.y = self.screen_rect.bottom - self.rect.height

