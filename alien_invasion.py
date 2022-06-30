import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height))
        self.screen_size = 'normal'

        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, 'Play')

        self.direction = ''

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.move(self.direction)
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, position):
        clicked_button = self.play_button.rect.collidepoint(position)
        if clicked_button and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            self.stats.reset_stats()
            self.scoreboard.prepare_score()
            self.scoreboard.prepare_level()
            self.scoreboard.prepare_lives()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.direction = 'right'
        elif event.key == pygame.K_LEFT:
            self.direction = 'left'
        elif event.key == pygame.K_UP:
            self.direction = 'up'
        elif event.key == pygame.K_DOWN:
            self.direction = 'down'
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_f:
            if self.screen_size == 'normal':
                self.screen_size = 'fullscreen'
                self._change_screen_size()
            else:
                self.screen_size = 'normal'
                self._change_screen_size()
        elif event.key == pygame.K_r:
            self.__init__()

    def _check_keyup_events(self, event):
        if (event.key == pygame.K_RIGHT
                or event.key == pygame.K_LEFT
                or event.key == pygame.K_UP
                or event.key == pygame.K_DOWN):
            self.direction = 'stop'

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_alien(self, alien_number, row_number):
        new_alien = Alien(self)
        new_alien_width, new_alien_height = new_alien.rect.size

        new_alien.x = new_alien_width + 2 * new_alien_width * alien_number
        new_alien.rect.x = new_alien.x

        new_alien.y = 3 * new_alien_height + 2 * new_alien_height * row_number
        new_alien.rect.y = new_alien.y

        self.aliens.add(new_alien)

    def _create_fleet(self):
        new_alien = Alien(self)
        new_alien_width, new_alien_height = new_alien.rect.size
        ship_height = self.ship.rect.height

        available_horizontal_space = \
            self.settings.screen_width - (2 * new_alien_width)
        available_vertical_space = \
            self.settings.screen_height - (5 * new_alien_height) \
            - ship_height

        number_of_aliens_horizontally = \
            available_horizontal_space // (2 * new_alien_width)
        number_of_rows_vertically = \
            available_vertical_space // (2 * new_alien_height)

        for row_number in range(number_of_rows_vertically):
            for alien_number in range(number_of_aliens_horizontally):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edge_position(self):
        for alien in self.aliens.sprites():
            if alien.check_position():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_bottom_collision(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_bullet_collision(self):
        bullet_collisions = pygame.sprite.groupcollide(self.bullets,
                                                       self.aliens,
                                                       True, True)

        if bullet_collisions:
            for aliens in bullet_collisions.values():
                self.stats.game_score += self.settings.alien_points \
                                         * len(aliens)

            self.scoreboard.prepare_score()
            self.scoreboard.check_high_score()

    def _check_ship_collision(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        if self.stats.lives_remaining > 0:
            self.stats.lives_remaining -= 1
            self.scoreboard.prepare_lives()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        self._check_fleet_edge_position()
        self.aliens.update()

        self._check_ship_collision()
        self._check_fleet_bottom_collision()

        if not self.aliens:
            sleep(1)

            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.game_level += 1
            self.scoreboard.prepare_level()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_collision()

    def _update_screen(self):
        self.screen.fill(self.settings.primary_color)
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _change_screen_size(self):
        if self.screen_size == 'normal':
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width,
                 self.settings.screen_height))
            self.ship.get_screen_size(self)
        else:
            self.screen = pygame.display.set_mode((0, 0),
                                                  pygame.FULLSCREEN)
            self.ship.get_screen_size(self)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
