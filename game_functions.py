import sys
import pygame
from bullet import Bullet
from alien import Alien


# группа функций работы с вводом данных
def check_events_k(event, ship, ai_settings, screen, bullets):
    '''Реагирует на нажатие и отпускание клавиш'''
    if event.type == pygame.KEYDOWN:
        check_event_key(event, ship, ai_settings, screen, bullets, True)
    elif event.type == pygame.KEYUP:
        check_event_key(event, ship, ai_settings, screen, bullets, False)


def check_event_key(event, ship, ai_settings, screen, bullets, result):
    if event.key == pygame.K_LEFT:
        ship.moving_left = result
    if event.key == pygame.K_RIGHT:
        ship.moving_right = result
    if event.key == pygame.K_SPACE and result == True:
        fire_bullet(ship, ai_settings, screen, bullets)


def check_events(ship, ai_settings, screen, bullets):
    '''отслеживание событий клавиатуры и мыши'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            check_events_k(event, ship, ai_settings, screen, bullets)


# функции отрисовки
def update_screen(ai_settings, screen, ship, bullets, aliens):
    '''обновляет отрисовку экрана и объектов'''
    # перерисовка экрана
    screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.bg_image, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Отображение последних событий на экране
    pygame.display.flip()


def update_bullets(bullets):
    '''обновление позиции пуль и удаление старых'''
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


# игровые механики
def fire_bullet(ship, ai_settings, screen, bullets):
    '''выпускать пулю если максимум ещё не достигнут'''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width) -> int:
    '''вычисление пришельцев в ряду'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settinggs, ship_height, alien_height):
    '''определение количество рядов,помещающихся на экран'''
    available_space_y = (ai_settinggs.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, aline_number, row_number):
    '''Создает пришельца и размещает его в ряду'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * aline_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    '''Создание флота противника'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for aline_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, aline_number, row_number)


# def move_fleet(ai_settings,):
