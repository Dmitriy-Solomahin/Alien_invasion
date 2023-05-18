from button import Button
import pygame

class MainMenu():
    '''Главное меню'''
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

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
        self.stats_button = Button(screen, 'Stats', 35)
        self.settings_button = Button(screen, 'Settings', -35)
        self.exit_button = Button(screen, 'Exit', -105)

    def draw_menu(self):
        '''Отрисовка меню'''
        self.screen.blit(self.Alien_invasion_image, self.Alien_invasion_rect)
        self.play_button.draw_button()
        self.stats_button.draw_button()
        self.settings_button.draw_button()
        self.exit_button.draw_button()
