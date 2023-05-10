import pygame

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
        high_score_str = Scoreboard.formating_score(self.stats.high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, None)
        
        self.high_score_rect = self.score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = 40 + self.font_size


    def show_score(self):
        '''Вывод счета на экран'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
