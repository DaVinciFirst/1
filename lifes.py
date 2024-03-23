import pygame
import os
from pygame.sprite import Sprite

class Lifes(Sprite):
    def __init__(self, aw_settings):
        super().__init__()
        self.aw_settings = aw_settings
        self.image = pygame.transform.scale(pygame.image.load(aw_settings.path_to_img + os.sep + "ship.png"), (aw_settings.alien_width // 1.5, aw_settings.alien_height // 1.5))
        self.rect = self.image.get_rect()