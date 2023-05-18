from button import Button


class Menu():
    '''Меню паузы'''
    def __init__(self, screen):
# создание кнопок
        self.resume_button = Button(screen, 'Resume', 70)
        self.restart_button = Button(screen, 'Restart', 0)
        self.exit_menu_button = Button(screen, 'Main menu', -70)

    def draw_menu(self):
        '''Отрисовка меню'''
        self.resume_button.draw_button()
        self.restart_button.draw_button()
        self.exit_menu_button.draw_button()
