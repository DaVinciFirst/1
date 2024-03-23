import pygame
from settings import Settings
from bg import Background
from ship import Ship
import game_func as gf
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import ScoreBoard
from strings import Strings


def run_game():
    pygame.init()
    aw_settings = Settings()
    stats = GameStats(aw_settings)
    screen = pygame.display.set_mode((aw_settings.screen_width, aw_settings.screen_height))
    strings = Strings(screen)
    sb = ScoreBoard(aw_settings, screen, stats)
    pygame.display.set_caption("Alien War")
    bground = Background(aw_settings, screen)
    ship = Ship(aw_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(aw_settings, screen, aliens, ship)
    menu = gf.create_menu(aw_settings, screen)
    gf.menu_sound()
    clock = pygame.time.Clock()
    while True:
        gf.check_events(ship, aw_settings, screen, bullets, stats, aliens, sb, menu)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, aw_settings, screen, ship, stats, sb)
            gf.update_aliens(aw_settings, aliens, ship, stats, screen, bullets, sb)
        gf.update_screen(bground, stats, screen, ship, bullets, aliens, sb, strings, menu)
        clock.tick(60)


if __name__ == "__main__":
    run_game()
