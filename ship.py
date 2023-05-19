import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen, size):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_multiplier = ai_settings.get_multiplier()
        self.size = (size[0] * self.screen_multiplier[0], size[1] * self.screen_multiplier[1])

        # создание внешнего вида карабля и вычесление размеров экрана и карабля
        self.image = pygame.transform.scale((pygame.image.load(
            'textures/rocket2_128p.png')), self.size)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # self.sound_shooting = 'sounds\warfare-laser-blast_fjdw5t4u.mp3'

        # Позиционирование корабля по центру снизу экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False


    def center_ship(self):#!!!!!!
        '''размещение корабля в стартовую позицию'''
        self.center = self.screen_rect.centerx


    def update(self):
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center


    def blitme(self):
        self.screen.blit(self.image, self.rect)
