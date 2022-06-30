import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = None
        self.get_screen_size(ai_game)
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/rocket_2.bmp')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def move(self, direction):
        if direction == 'right':
            self.check_and_move(self.x, 1)
        elif direction == 'left':
            self.check_and_move(self.x, -1)
        elif direction == 'up':
            self.check_and_move(self.y, -1)
        elif direction == 'down':
            self.check_and_move(self.y, 1)

        self.rect.x = self.x
        self.rect.y = self.y

    def check_and_move(self, axis, direction):
        if axis == self.x:
            if (self.rect.left > self.screen_rect.left and direction == -1) \
                    or (self.rect.right < self.screen_rect.right and direction == 1):
                self.x += direction * self.settings.ship_speed
                return self.x
            else:
                return self.x
        elif axis == self.y:
            if (self.rect.top > self.screen_rect.top and direction == -1) \
                    or (self.rect.bottom < self.screen_rect.bottom and direction == 1):
                self.y += direction * self.settings.ship_speed
                return self.y
            else:
                return self.y

    def get_screen_size(self, ai_game):
        self.screen = ai_game.screen
