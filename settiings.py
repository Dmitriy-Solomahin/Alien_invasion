import pygame


class Settings():

    def __init__(self):
        '''Инициализирует статические настройки игры'''
        # настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_image = pygame.transform.scale((pygame.image.load(
            "textures/bg.jpg")), (self.screen_width, self.screen_height))
        self.bg_color = (106, 90, 205)

        # настройки карабля
        self.ship_limit = 3

        # настройки пули
        self.bullet_wigth = 3000
        self.bullet_height = 15
        self.bullet_color = 255, 250, 205
        self.bullets_allowed = 5

        # настройки пришельцев
        self.fleet_drop_speed = 10
        
        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста очков
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''Инициализация настроек, изменяемых в ходе игры'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        self.fleet_direction = 1 # направление движения флота 1 вправо -1 влево
        
        # подсчёт очков
        self.alien_points = 10


    def increase_speed(self):
        '''Увеличение динамических настроек'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
