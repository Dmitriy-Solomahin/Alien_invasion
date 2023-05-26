class GameStats():
    '''Отслеживание статистики по игре'''
    
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        
        self.game_active = False
        self.records_menu = False
        self.game_PAUSE = False
        
        self.score = 0
        self.settings_fille = 'program\settings_fille.txt'
        self.high_score = []
        self.open_file()
        self.now_high_score = self.high_score[0]
        self.reset_stats()

    def reset_stats(self):
        '''Статистика меняющаяся в ходе игры'''
        self.ships_left = self.ai_settings.ship_limit
        # self.checking_records()
        self.score = 0
        self.level = 1

    def open_file(self):
        '''Загрузка статистики из файла'''
        with open(self.settings_fille, 'r', encoding='UTF-8') as file:
            data = file.readlines()
            self.high_score = [int(i) for i in data[0].strip().split(';')]


    def checking_records(self):
        '''Проверка рекордной сетки'''
        for i in range(len(self.high_score)):
            if self.score > self.high_score[i]:
                self.high_score.insert(i, self.score)
                if len(self.high_score) > 5:
                    self.high_score.pop(5)
                    self.overwriting_file()
                    break

    def overwriting_file(self):
        '''Перезапись файла с рекордами'''
        s = [str(i) for i in self.high_score]
        data = ';'.join(s)
        with open(self.settings_fille, 'w', encoding='UTF-8') as file:
            file.write(data)


    def formating_record(self):
        '''Преобразует список рекордов в таблицу'''
        lines = []
        for i in range(len(self.high_score)):
            lines.append(str(i+1) + ': ' + str(self.high_score[i]))
        return lines