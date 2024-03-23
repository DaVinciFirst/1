import pygame.image
import os

class Background():
    def __init__(self, aw_settings, screen):
        self.aw_settings = aw_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        image = pygame.image.load(aw_settings.path_to_img + os.sep + "space.png")
        self.space_img = pygame.transform.scale(image, (aw_settings.screen_width, aw_settings.screen_height))
        self.space_img2 = pygame.transform.scale(image, (aw_settings.screen_width, aw_settings.screen_height))
        self.rect = self.space_img.get_rect()
        self.rect2 = self.space_img.get_rect()
        self.rect.y = 0
        self.rect2.y = self.rect.y - self.rect.height

    def blitme(self):
        if self.rect.top >= self.screen_rect.bottom or self.rect2.top >= self.screen_rect.bottom:
            self.rect.y = 0
            self.rect2.y = self.rect.y - self.rect.height
        else:
            self.rect.y += 5
            self.rect2.y += 5
        self.rect.height = self.rect.y
        self.rect2.height = self.rect2.y
        self.screen.blit(self.space_img, self.rect)
        self.screen.blit(self.space_img2, self.rect2)

