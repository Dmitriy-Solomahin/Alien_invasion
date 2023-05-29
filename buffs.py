from random import choice

import pygame


class Buffs():

    def __init__(self, ai_settings, screen, stats, sb) -> None:
        # константы
        self.BUFFS = {
            0: ['textures/icon/repair.png', 'Repair ship'],
            1: ['textures/icon/bullet.png', 'Bullet upgrade'],
            2: ['textures/icon/gun.png', 'Gan upgrade'],
            3: ['textures/icon/speed.png', 'Debuff speed alien']}
        self.SIZE = (64, 64)

        #
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats
        # self.ship = ship
        self.sb = sb
        self.screen_multiplier = ai_settings.get_multiplier()
        self.size = (self.SIZE[0] * self.screen_multiplier[0],
                     self.SIZE[1] * self.screen_multiplier[1])

        # базовые параметры
        self.buff = choice(self.BUFFS)
        self.buff_text = self.buff[1]
        self.buff_image = pygame.transform.scale(
            (pygame.image.load(self.buff[0])), self.size)
        self.buff_image_rect = self.buff_image.get_rect()
        


    def __eq__(self, __value: object) -> bool:
        if self.buff_text == __value.buff_text:
            return True
        return False


    def use_buff(self):
        '''применение бонуса'''
        if self.buff_text == 'Repair ship':
            self.stats.ships_left += 1
            self.sb.prep_ships()
        elif self.buff_text == 'Bullet upgrade':
            self.ai_settings.bullet_wigth = 5
            self.ai_settings.bullet_height = 20
            self.ai_settings.level_bullet += 1
        elif self.buff_text == 'Gan upgrade':
            self.ai_settings.level_gun += 1
            self.ai_settings.bullets_allowed += 5
        elif self.buff_text == 'Debuff speed alien':
            self.ai_settings.alien_speed_factor //= 1.5
            
