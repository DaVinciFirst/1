import pygame

class Menu():

    def __init__(self, aw_settings, screen, text, pos):
        self.hovered = False
        self.aw_settings = aw_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = self.aw_settings.menu_button_width, self.aw_settings.menu_button_height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.text = text
        self.pos = pos
        self.font = pygame.font.SysFont(None, 40)
        self.text_color = (100, 154, 252)
        self.text_color_hovered = (0, 0, 255)
        self.sound_lim = 0

        self.play_button_pos = (self.screen_rect.centerx, self.aw_settings.alien_height * 5.5)
        self.setting_button_pos = (self.screen_rect.centerx, self.aw_settings.alien_height * 6.5)
        self.exit_button_pos = (self.screen_rect.centerx, self.aw_settings.alien_height * 7.5)
        self.draw()

    def draw(self):
        if self.hovered:
            self.point = self.font.render(self.text, True, self.text_color_hovered)
        else:
            self.point = self.font.render(self.text, True, self.text_color)
        self.rect.centerx, self.rect.top = self.pos
        self.point_rect = self.point.get_rect()
        self.point_rect.centerx = self.rect.centerx
        self.point_rect.centerx, self.point_rect.top = self.pos
        self.screen.blit(self.point, self.point_rect)




