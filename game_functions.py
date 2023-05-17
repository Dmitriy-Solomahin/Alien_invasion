import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


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


def check_events(ai_settings, screen, ship, bullets, stats, aliens, sb, play_button):
    '''отслеживание событий клавиатуры и мыши'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            check_events_k(event, ship, ai_settings, screen, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, bullets,
                            stats, aliens, sb, play_button, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, ship, bullets, stats, aliens, sb, play_button, mouse_x, mouse_y):
    '''Запускает новую игру при нажатии кнопки Play'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings() # сброс игровой статистики
        pygame.mouse.set_visible(False)  # скрывает указатель мыши
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        game_restart(ai_settings, screen, ship, bullets, aliens)


# функции отрисовки
def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb):
    '''обновляет отрисовку экрана и объектов'''
    # перерисовка экрана
    screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.bg_image, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # Отображение последних событий на экране
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    '''обновление позиции пуль и удаление старых'''
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullets_alien_collisions(
        bullets, aliens, ai_settings, screen, ship, stats, sb)


def check_bullets_alien_collisions(bullets, aliens, ai_settings, screen, ship, stats, sb):
    '''Обработка колизий пуль с пришельцами'''
    # Проверка попадания в пришельцев
    # При обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        filling_fleet(ai_settings, screen, aliens, ship, bullets, stats, sb)


def check_high_score(stats, sb):
    '''Проверяет обновление рекорда'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def filling_fleet(ai_settings, screen, aliens, ship, bullets, stats, sb):
    '''Вызов подкрепления'''
    # Уничтожение оставшихся пуль и создание нового флота ускоряя его
    bullets.empty()
    ai_settings.increase_speed()
    # увеличивает уровень
    stats.level += 1
    sb.prep_level()
    
    create_fleet(ai_settings, screen, aliens, ship)


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
    available_space_y = (ai_settinggs.screen_height -
                         (3 * alien_height) - ship_height)
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
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for aline_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, aline_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    '''проверяет достиг ли кто либо из пришелецев края экрана'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Опускает весь флот вниз и меняет направлениеего движения'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, ship, bullets, aliens, stats, sb):
    '''Обрабатывает столкновение карабля с пришельцем'''
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        game_restart(ai_settings, screen, ship, bullets, aliens)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def game_restart(ai_settings, screen, ship, bullets, aliens):
    '''Подготовка игры к старту'''
    # отчиска поля
    aliens.empty()
    bullets.empty()
    # востановление корабля в стартовой точке и создаёт флот заново
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()
    # пауза
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, ship, bullets, aliens, stats, sb):
    '''проверка достиг ли пришелец низа экрана'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, ship, bullets, aliens, stats, sb)
            break


def update_alinse(ai_settings, screen, ship, bullets, aliens, stats, sb):
    '''обновление позиции всех пришельцев во флоте'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, bullets, aliens, stats, sb)

    check_aliens_bottom(ai_settings, screen, ship, bullets, aliens, stats, sb)
