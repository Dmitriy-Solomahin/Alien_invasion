from button import Button
import pygame


class MainMenu():
    '''Главное меню'''

    def __init__(self, screen, sb):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.sb = sb

# Изображение названия
        self.font = pygame.font.SysFont(None, 96)
        self.Alien_invasion_image = self.font.render(
            "Alien Invasion", True, (238, 201, 0), None)
# расположение названия
        self.Alien_invasion_rect = self.Alien_invasion_image.get_rect()
        self.Alien_invasion_rect.center = self.screen_rect.center
        self.Alien_invasion_rect.top = 50
# Создание кнопок
        self.play_button = Button(screen, 'Play', 105)
        self.records_button = Button(screen, 'Records', 35)
        self.settings_button = Button(screen, 'Settings', -35)
        self.exit_button = Button(screen, 'Exit', -105)
        self.back_button = Button(screen, 'Back', -250)

    def draw_menu(self):
        '''Отрисовка меню'''
        self.screen.blit(self.Alien_invasion_image, self.Alien_invasion_rect)
        self.play_button.draw_button()
        self.records_button.draw_button()
        self.settings_button.draw_button()
        self.exit_button.draw_button()

    def draw_records(self):
        '''Отрисовка рекордов'''
        self.back_button.draw_button()
        self.sb.show_records_table()
