import pygame.font

class Strings():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.prep_name()
        self.prep_footer()

    def prep_footer(self):
        footer_str = "Made by DaVinci @ 2022"
        text_color = (255, 255, 228)
        self.font = pygame.font.SysFont(None, 25)
        self.footer_image = self.font.render(footer_str, True, text_color)
        self.footer_rect = self.footer_image.get_rect()
        self.footer_rect.centerx = self.screen_rect.centerx
        self.footer_rect.bottom = self.screen_rect.bottom - 10

    def prep_name(self):
        name_str = "ALIEN WAR"
        text_color = (252, 1, 10)
        self.font = pygame.font.SysFont(None, 100)
        self.name_image = self.font.render(name_str, True, text_color)
        self.name_rect = self.name_image.get_rect()
        self.name_rect.left = self.screen_rect.left + 40
        self.name_rect.top = self.name_rect.top + 40

    def show_strings(self):
        self.screen.blit(self.footer_image, self.footer_rect)
        self.screen.blit(self.name_image, self.name_rect)