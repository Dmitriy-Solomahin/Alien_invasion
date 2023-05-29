from typing import Any
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''Класс описывающий пришелеца'''


    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_multiplier = ai_settings.get_multiplier()
        self.size = (64 * self.screen_multiplier[0],
                     64 * self.screen_multiplier[1])

        self.image = pygame.transform.scale((pygame.image.load(
            'textures/enemy/Enemy1_128p.png')), self.size)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def check_edges(self) -> bool:
        '''проверяет достиг ли пришелец края экрана'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False


    def update(self):
        '''изменение позиции пришельца'''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        '''Выводит пришельца в его текущей позиции'''
        self.screen.blit(self.image, self.rect)
