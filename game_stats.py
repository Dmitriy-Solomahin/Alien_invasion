class GameStats():
    '''Отслеживание статистики по игре'''
    
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        
        self.game_active = False

    def reset_stats(self):
        '''Статистика меняющаяся в ходе игры'''
        self.ships_left = self.ai_settings.ship_limit