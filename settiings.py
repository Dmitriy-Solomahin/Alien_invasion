import pygame


class Settings():

    def __init__(self, screen):
        '''Инициализирует статические настройки игры'''
        # настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.height_multiplier = self.screen_rect.height / self.screen_height
        self.width_multiplier = self.screen_rect.width / self.screen_width
        self.active_screen_w = self.screen_width * self.width_multiplier
        self.active_screen_h = self.screen_height * self.height_multiplier
        self.bg_image = pygame.transform.scale((pygame.image.load(
            "textures/bg/bg.jpg")), (self.screen_rect.width, self.screen_rect.height))
        self.bg_color = (106, 90, 205)

        # настройки музыки
        self.menu_sound = 'sounds/gspr-nightcall.mp3'
        # self.game_sound = ''
        self.sound_shooting = 'sounds/warfare-laser-blast_fjdw5t4u.mp3'
        self.sound_destruction = 'sounds/aa8b64ca38f350.mp3'
        self.sound_signal = 'sounds/b5ba5fcc1a93887.mp3'
        self.sound_losing = 'sounds/fail-wha-wha-version.mp3'

        # настройки пули
        self.bullet_color = 255, 250, 205


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

        # настройки карабля
        self.ship_limit = 3
        self.level_gun = 1
        
        
        # настройки пули
        self.level_bullet = 1
        self.bullet_wigth = 3000
        self.bullet_height = 15
        self.bullets_allowed = 5
        
        # подсчёт очков
        self.alien_points = 10


    def increase_speed(self):
        '''Увеличение динамических настроек'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)

    def get_multiplier(self):
        return (self.width_multiplier, self.height_multiplier)
