import sys
import pygame
from pygame import mixer
from bullet import Bullet
from alien import Alien
from time import sleep
from buffs import Buffs

# РАБОТА С ВВЕДЁННЫМИ ДАННЫМИ
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


def check_events(ai_settings, screen, ship, bullets, stats, aliens, sb, main_menu, menu):
    '''отслеживание событий клавиатуры и мыши'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.checking_records()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and stats.game_active and not stats.game_PAUSE:
            stats.game_PAUSE = True
            pygame.mouse.set_visible(True)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and stats.game_active and stats.game_PAUSE:
            stats.game_PAUSE = False
            pygame.mouse.set_visible(False)
        elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and stats.game_active:
            check_events_k(event, ship, ai_settings, screen, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, bullets,
                            stats, aliens, sb, main_menu, menu, mouse_x, mouse_y)
            check_exit_button(stats, main_menu, mouse_x, mouse_y)
            check_main_menu_button(stats, menu, mouse_x, mouse_y)
            check_resume_button(stats, menu, mouse_x, mouse_y)
            check_back_button(stats, main_menu, mouse_x, mouse_y)
            check_records_button(stats, main_menu, mouse_x, mouse_y)
            if stats.buff_pause:
                check_buff_clicked(stats, sb, mouse_x, mouse_y)


# РАБОТА С КНОПКАМИ
def check_play_button(ai_settings, screen, ship, bullets, stats, aliens, sb, main_menu, menu, mouse_x, mouse_y):
    '''Запускает новую игру при нажатии кнопки Play или кнопки Restart'''
    button_clicked = main_menu.play_button.rect.collidepoint(mouse_x, mouse_y)
    button_pause_clicked = menu.restart_button.rect.collidepoint(
        mouse_x, mouse_y)
    if (button_clicked and not stats.game_active and not stats.records_menu) or (button_pause_clicked and stats.game_PAUSE):
        ai_settings.initialize_dynamic_settings() # сброс игровой статистики
        pygame.mouse.set_visible(False)  # скрывает указатель мыши
        stats.reset_stats()
        stats.game_active = True
        stats.game_PAUSE = False
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        game_restart(ai_settings, screen, ship, bullets, aliens)


def check_records_button(stats, main_menu, mouse_x, mouse_y):
    '''Открывает таблицу рекордов если нажата кнопка Records'''
    button_clicked = main_menu.records_button.rect.collidepoint(
        mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not stats.records_menu:
        stats.records_menu = True


def check_exit_button(stats, main_menu, mouse_x, mouse_y):
    '''Выход из игры если нажата кнопка Exit'''
    button_clicked = main_menu.exit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not stats.records_menu:
        sys.exit()


def check_back_button(stats, main_menu, mouse_x, mouse_y):
    '''Возвращается в главное меню после нажатия кнопки назад'''
    button_clicked = main_menu.back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and stats.records_menu:
        stats.records_menu = False


def check_main_menu_button(stats, menu, mouse_x, mouse_y):
    '''Выход в главное меню при нажатии кнопки Main Menu'''
    button_clicked = menu.exit_menu_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.game_PAUSE:
        stats.game_PAUSE = False
        stats.game_active = False
        stats.checking_records()


def check_resume_button(stats, menu, mouse_x, mouse_y):
    '''Продолжить игру при нажатии кнопки Resume'''
    button_clicked = menu.resume_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.game_PAUSE:
        stats.game_PAUSE = False


def check_buff_clicked(stats, sb, mouse_x, mouse_y):
    '''Проверка нажатия на бафф и применение его'''
    button_clicked_1 = sb.buff_1.buff_image_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked_1 :
        sb.buff_1.use_buff()
        pygame.mouse.set_visible(False)
        stats.buff_pause = False
    button_clicked_2 = sb.buff_2.buff_image_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked_2 :
        sb.buff_2.use_buff()
        pygame.mouse.set_visible(False)
        stats.buff_pause = False


# ФУНКЦИИ ОТРИСОВКИ
def update_screen(ai_settings, screen, ship, bullets, aliens, stats, sb, main_menu, menu):
    '''обновляет отрисовку экрана и объектов'''
    # перерисовка экрана
    screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.bg_image, (0, 0))
    if stats.game_active:
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        
        sb.show_score()

    if not stats.game_active:
        if stats.records_menu:
            main_menu.draw_records()
        else:
            main_menu.draw_menu()
    
    if stats.buff_pause:
        sb.show_buffs()

    if stats.game_PAUSE:
        menu.draw_menu()

    # Отображение последних событий на экране
    pygame.display.flip()


# РАБОТА СО СНАРЯДАМИ
def fire_bullet(ship, ai_settings, screen, bullets):
    '''выпускать пулю если максимум ещё не достигнут'''
    if len(bullets) < ai_settings.bullets_allowed:
        bullet_Sound = mixer.Sound(ai_settings.sound_shooting)
        bullet_Sound.play()
        for i in range(ai_settings.level_gun):
            if ai_settings.level_gun == 2:
                new_bullet = Bullet(ai_settings, screen, ship, i+2)
            else:
                new_bullet = Bullet(ai_settings, screen, ship, i+1)
            bullets.add(new_bullet)

def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    '''обновление позиции пуль и удаление старых'''
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullets_alien_collisions(
        bullets, aliens, ai_settings, screen, ship, stats, sb)


# ОБРАБОТКА КОЛИЗИЙ
def check_bullets_alien_collisions(bullets, aliens, ai_settings, screen, ship, stats, sb):
    '''Обработка колизий пуль с пришельцами'''
    # Проверка попадания в пришельцев
    # При обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for bullet, alien in collisions.items():
            if bullet.bullet_heals == 1:
                bullets.remove(bullet)
            else:
                bullet.bullet_heals -= 1
            destruction_Sound = mixer.Sound(ai_settings.sound_destruction)
            destruction_Sound.play()
            stats.score += ai_settings.alien_points #* len(aliens) зачем?
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        filling_fleet(ai_settings, screen, aliens, ship, bullets, stats, sb)


def ship_hit(ai_settings, screen, ship, bullets, aliens, stats, sb):
    '''Обрабатывает столкновение карабля с пришельцем'''
    if stats.ships_left > 0:
        restart_Sound = mixer.Sound(ai_settings.sound_signal)
        restart_Sound.play()
        stats.ships_left -= 1
        sb.prep_ships()
        game_restart(ai_settings, screen, ship, bullets, aliens)
    else:
        game_over_Sound = mixer.Sound(ai_settings.sound_losing)
        game_over_Sound.play()
        stats.game_active = False
        stats.checking_records()
        pygame.mouse.set_visible(True)


# РАБОТА С ПРОТИВНИКОМ

# расчет числа пришельцев
def get_number_aliens_x(ai_settings, alien_width) -> int:
    '''вычисление пришельцев в ряду'''
    available_space_x = ai_settings.active_screen_w - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settinggs, ship_height, alien_height):
    '''определение количество рядов,помещающихся на экран'''
    available_space_y = (ai_settinggs.active_screen_h -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

# добавление пришельцев
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


def filling_fleet(ai_settings, screen, aliens, ship, bullets, stats, sb):
    '''Вызов подкрепления'''
    # Уничтожение оставшихся пуль и создание нового флота ускоряя его
    bullets.empty()
    ai_settings.increase_speed()
    # увеличивает уровень
    stats.level += 1
    # вызов бафов каждый 5й уровень
    if stats.level % 5 == 0:
        choosing_buffs(ai_settings, screen, stats, sb)
        stats.buff_pause = True
        pygame.mouse.set_visible(True)
        
    sb.prep_level()
    
    create_fleet(ai_settings, screen, aliens, ship)


# движение противника
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


# ОБЩЕИГРОВЫЕ ФУНКЦИИ
def game_restart(ai_settings, screen, ship, bullets, aliens):
    '''Подготовка игры к старту'''
    # отчиска поля
    aliens.empty()
    bullets.empty()
    # востановление корабля в стартовой точке и создаёт флот заново
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()
    # пауза
    sleep(1)


def check_high_score(stats, sb):
    '''Проверяет обновление рекорда'''
    if stats.score > stats.now_high_score:
        stats.now_high_score = stats.score
        sb.prep_high_score()


def choosing_buffs(ai_settings, screen, stats, sb):
    '''создание бафов'''
    buff_1 = Buffs(ai_settings, screen, stats, sb)
    while True:
        buff_2 = Buffs(ai_settings, screen, stats, sb)
        if not buff_1 == buff_2:
            break
    sb.buff_1 = buff_1
    sb.buff_2 = buff_2