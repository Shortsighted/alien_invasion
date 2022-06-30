import pygame.font


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.primary_color = (10, 10, 15)
        self.secondary_color = (0, 255, 0)
        self.primary_font = pygame.font.SysFont(None, 48)

        self.ship_speed = 0.5
        self.total_lives = 3

        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 3

        self.alien_speed = 0.3
        self.fleet_drop_speed = 7
        self.fleet_direction = 1

        self.alien_points = 50
        self.game_speedup_scale = 1.1
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        self.ship_speed = 0.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.3

        self.alien_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.game_speedup_scale
        self.bullet_speed *= self.game_speedup_scale
        self.alien_speed *= self.game_speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
