class MemorySettings:
    def __init__(self, difficulty="easy"):
        self.screen_width = 800 # ширина окна
        self.screen_height = 600 # высота окна
        self.bg_color = (30, 30, 60) #цвет заливки

        # Настройки сложности
        self.difficulty = difficulty
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        if difficulty == 'easy':
            self.rows = 2
            self.cols = 4
            self.time_limit = 30  # лимит времени
            self.max_moves = 10 # лимит ходов
        elif difficulty == 'medium':
            self.rows = 4
            self.cols = 4
            self.time_limit = 40
            self.max_moves = 25
        elif difficulty == 'hard':
            self.rows = 4
            self.cols = 6
            self.time_limit = 60
            self.max_moves = 35
        elif difficulty == 'insane':
            self.rows = 6
            self.cols = 8
            self.time_limit = 80
            self.max_moves = 55

        self.total_cards = self.rows * self.cols