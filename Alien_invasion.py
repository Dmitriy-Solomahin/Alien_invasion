import pygame
import game_functions as gf
from pygame.sprite import Group
from settiings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # инициализация игры и создание экрана
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    play_button = Button(ai_settings, screen, 'Play')
    
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen, (64,64))
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings, screen, aliens, ship)

    # запеск основного процесса игы
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, aliens, sb, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings,
                                screen, ship, stats, sb)
            gf.update_alinse(ai_settings, screen, ship, bullets, aliens, stats, sb)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb)


run_game()
