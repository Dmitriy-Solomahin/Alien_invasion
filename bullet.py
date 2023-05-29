from typing import Any
import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    '''Клас для управления пулями'''


    def __init__(self, ai_settings, screen, ship, position):
        '''Создание обьекта пули в текущей позиции карабля'''
        super().__init__()
        self.screen = screen

        self.position = position
        self.position_ship = ship.rect
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_wigth, ai_settings.bullet_height)
        self.bullet_positioning()

        self.bullet_heals = ai_settings.level_bullet
        
        # позиция сохраняется в вещественном ввиде
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y


    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


    def bullet_positioning(self):
        '''Позицеонирование пули'''
        self.rect.top = self.position_ship.top
        if self.position == 1:
            self.rect.centerx = self.position_ship.centerx
        elif self.position == 2:
            self.rect.centerx = self.position_ship.left
            self.rect.top += 20
        elif self.position == 3:
            self.rect.centerx = self.position_ship.right
            self.rect.top += 20
