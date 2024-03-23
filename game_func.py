import sys
import os
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from menu import Menu

def check_keydown_events(event, ship, aw_settings, screen, bullets, stats):
    if event.key == pygame.K_ESCAPE:
        with open("config.cfg", "w") as conf:
            conf.write(str(stats.high_score))
        sys.exit()
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(aw_settings, screen, ship, bullets)
        shot_sound()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = False


def check_events(ship, aw_settings, screen, bullets, stats, aliens, sb, menu):
    for point in menu:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if point.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
            if not point.sound_lim:
                hover_sound()
                point.sound_lim += 1
            point.hovered = True
        else:
            point.hovered = False
            point.sound_lim = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for point in menu:
                if not stats.game_active and point.hovered:
                    choose_sound()
                    if point.text == "Новая игра":
                        pygame.mixer.music.stop()
                        aw_settings.initialize_dynamic_settings()
                        pygame.mouse.set_visible(False)
                        stats.reset_stats()
                        stats.game_active = True
                        sb.prep_score()
                        sb.prep_high_score()
                        sb.prep_level()
                        sb.prep_ships()
                        aliens.empty()
                        bullets.empty()
                        create_fleet(aw_settings, screen, aliens, ship)
                        ship.center_ship()
                        battle_sound()
                    elif point.text == "Настройки":
                        show_settings()
                    elif point.text == "Выход":
                        sleep(0.3)
                        sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, aw_settings, screen, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(bground, stats, screen, ship, bullets, aliens, sb, strings, menu):
    bground.blitme()
    if not stats.game_active:
        show_menu(menu)
        strings.show_strings()
    else:
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()
    pygame.display.flip()


def update_bullets(bullets, aliens, aw_settings, screen, ship, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(aw_settings, screen, ship, aliens, bullets, stats, sb)


def check_bullet_alien_collisions(aw_settings, screen, ship, aliens, bullets, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += aw_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ship.center_ship()
        aw_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        sleep(0.5)
        create_fleet(aw_settings, screen, aliens, ship)


def fire_bullet(aw_settings, screen, ship, bullets):
    if len(bullets) < aw_settings.bullets_allowed:
        new_bullet = Bullet(aw_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(aw_settings, screen, aliens, ship):
    alien = Alien(aw_settings, screen)
    number_aliens_x = get_number_aliens_x(aw_settings, alien.rect.width)
    number_rows = get_number_aliens_y(aw_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(aw_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(aw_settings, alien_width):
    available_space_x = aw_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x


def get_number_aliens_y(aw_settings, ship_height, alien_height):
    available_space_y = (aw_settings.screen_height - (4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(aw_settings, screen, aliens, alien_number, row_number):
    alien = Alien(aw_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def check_fleet_edges(aw_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(aw_settings, aliens)
            break


def change_fleet_direction(aw_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += aw_settings.fleet_drop_speed
    aw_settings.fleet_direction *= -1


def ship_hit(aw_settings, stats, screen, ship, aliens, bullets, sb):
    stats.ships_left -= 1
    if stats.ships_left > 0:
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(aw_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.reset_stats()
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(aw_settings, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(aw_settings, stats, screen, ship, aliens, bullets, sb)
            break


def update_aliens(aw_settings, aliens, ship, stats, screen, bullets, sb):
    check_fleet_edges(aw_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(aw_settings, stats, screen, ship, aliens, bullets, sb)
    check_aliens_bottom(aw_settings, stats, screen, ship, aliens, bullets, sb)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def create_menu(aw_settings, screen):
    m = Menu(aw_settings, screen, "", (0, 0))
    menu_points = [Menu(aw_settings, screen, "Новая игра", m.play_button_pos),
                   Menu(aw_settings, screen, "Настройки", m.setting_button_pos),
                   Menu(aw_settings, screen, "Выход", m.exit_button_pos)]
    del m
    return menu_points


def show_menu(menu):
    for point in menu:
        point.draw()


def show_settings():
    pass

def shot_sound():
    shot = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds") + os.sep + "shot.mp3")
    shot.play()

def menu_sound():
    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "sounds") + os.sep + "menu.mp3")
    pygame.mixer.music.play(-1, 0.0)

def battle_sound():
    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "sounds") + os.sep + "battle.mp3")
    pygame.mixer.music.play(-1, 0.0)

def choose_sound():
    choose = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds") + os.sep + "choose.mp3")
    choose.play()

def hover_sound():
    hover = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds") + os.sep + "hover.mp3")
    hover.play()
