import pygame


class Settings():

    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 800
        self.bg_image = pygame.transform.scale((pygame.image.load(
            "textures/bg.jpg")), (self.screen_width, self.screen_height))
        self.bg_color = (106, 90, 205)

        # настройки карабля
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # настройки пули
        self.bullet_speed_factor = 2
        self.bullet_wigth = 3
        self.bullet_height = 15
        self.bullet_color = 255, 250, 205
        self.bullets_allowed = 5

        # настройки пришельцев
        self.alien_speed_factor = 10
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # направление движения флота 1 вправо -1 влево