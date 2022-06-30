import pygame.font


class Button:
    def __init__(self, ai_game, message):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = ai_game.settings.secondary_color
        self.text_color = ai_game.settings.primary_color
        self.text_font = ai_game.settings.primary_font

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prepare_message(message)

    def _prepare_message(self, message):
        self.message_image = self.text_font.render(message,
                                                   True,
                                                   self.text_color,
                                                   self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
