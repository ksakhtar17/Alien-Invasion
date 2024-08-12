import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """class to manage the ship"""
    def __init__(self, ai_game, img):
        """initialize the ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # to get the dimensions of the screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load(img)
        # to get the dimensions of the image
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        # store a float for  a ship exact horizontal position
        self.x = float(self.rect.x)

        # movement flag; start with a ship that is not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """update the ship's position based in the movement flag"""
        # update ship's x value not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
