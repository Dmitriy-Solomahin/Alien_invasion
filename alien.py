import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''Класс описывающий пришелеца'''


    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.image = pygame.transform.scale((pygame.image.load(
            'textures/Enemy1_128p.png')), (64,64))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def blitme(self):
        '''Выводит пришельца в его текущей позиции'''
        self.screen.blit(self.image, self.rect)
