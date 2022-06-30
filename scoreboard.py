from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = self.ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = self.ai_game.settings
        self.stats = self.ai_game.stats

        self.high_score = 0

        self.prepare_score()
        self.prepare_high_score()
        self.prepare_level()
        self.prepare_lives()

    def prepare_score(self):
        rounded_score = round(self.stats.game_score, -1)
        score_string = '{:,}'.format(rounded_score)
        self.score_image = \
            self.settings.primary_font.render(score_string,
                                              True,
                                              self.settings.secondary_color,
                                              self.settings.primary_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prepare_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = '{:,}'.format(high_score)
        self.high_score_image = self.settings.primary_font.render(high_score_str,
                                                                  True,
                                                                  self.settings.secondary_color,
                                                                  self.settings.primary_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prepare_level(self):
        game_level_string = str(self.stats.game_level)
        self.game_level_image = self.settings.primary_font.render(game_level_string,
                                                                  True,
                                                                  self.settings.secondary_color,
                                                                  self.settings.primary_color)

        self.game_level_rect = self.game_level_image.get_rect()
        self.game_level_rect.right = self.score_rect.right
        self.game_level_rect.top = self.score_rect.bottom + 10

    def prepare_lives(self):
        self.ships = Group()
        for lives_left in range(self.stats.lives_remaining):
            life = Ship(self.ai_game)
            life.rect.x = 10 + lives_left * life.rect.width
            life.rect.y = 10
            self.ships.add(life)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.game_level_image, self.game_level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        if self.stats.game_score > self.stats.high_score:
            self.stats.high_score = self.stats.game_score
            self.prepare_high_score()


