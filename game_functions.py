import sys
import pygame
from bullet import Bullet


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


def fire_bullet(ship, ai_settings, screen, bullets):
    '''выпускать пулю если максимум ещё не достигнут'''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_events(ship, ai_settings, screen, bullets):
    '''отслеживание событий клавиатуры и мыши'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            check_events_k(event, ship, ai_settings, screen, bullets)


def update_screen(ai_settings, screen, ship, bullets):
    '''обновляет отрисовку экрана и объектов'''
    # перерисовка экрана
    screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.bg_image, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    # Отображение последних событий на экране
    pygame.display.flip()


def update_bullets(bullets):
    '''обновление позиции пуль и удаление старых'''
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
