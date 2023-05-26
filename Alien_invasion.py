import pygame
import game_functions as gf
from pygame.sprite import Group
from settiings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from main_menu import MainMenu
from menu import Menu
from pygame import mixer


def run_game():
    # инициализация игры и создание экрана
    pygame.init()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

    ai_settings = Settings(screen)
    pygame.display.set_caption("Alien Invasion")

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    main_menu = MainMenu(screen, sb)
    menu = Menu(screen)

    ship = Ship(ai_settings, screen, (64,64))
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings, screen, aliens, ship)

    mixer.music.load(ai_settings.menu_sound)
    mixer.music.play(-1)
    # запуск основного процесса игы
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, aliens,
                        sb, main_menu, menu)
        if stats.game_active and not stats.game_PAUSE:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings,
                                screen, ship, stats, sb)
            gf.update_alinse(ai_settings, screen, ship, bullets, aliens, stats, sb)
        gf.update_screen(ai_settings, screen, ship, bullets,
                        aliens, stats, sb, main_menu, menu)


run_game()
