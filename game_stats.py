class GameStats:
    def __init__(self, ai_game):
        self.lives_remaining = 0
        self.game_score = 0
        self.game_level = 0
        self.high_score = 0
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False

    def reset_stats(self):
        self.lives_remaining = self.settings.total_lives
        self.game_score = 0
