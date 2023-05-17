import pygame
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    '''Класс для вывода игровой информации'''

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # настройки шрифта
        self.font_size = 48
        self.text_color = (255, 255, 224)
        self.font = pygame.font.SysFont(None, self.font_size)
        # подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''преобразует текущий счёт в графический вид'''
        score_str = Scoreboard.formating_score(self.stats.score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, None)

        # вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    @staticmethod
    def formating_score(score) -> str:
        rounded_score = int(round(score, -1))
        score_str = '{:,}'.format(rounded_score)
        return score_str


    def prep_high_score(self):
        '''преобразует максимальный счёт в графический вид'''
        high_score_str = Scoreboard.formating_score(self.stats.high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, None)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.top = 20


    def prep_level(self):
        '''преобразует текущий лэвэл в графический вид'''
        self.level_image = self.font.render(
            str(self.stats.level), True, self.text_color, None)
        
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 40 + self.score_rect.height


    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen, (32,32))
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show_score(self):
        '''Вывод счета на экран'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
