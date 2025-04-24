import pygame  # Импортируем библиотеку Pygame для создания графического интерфейса
from game import MemorySettings
from game.memory_game import start_memory_game

class MainMenu:
    def __init__(self, screen):
        """
        Конструктор главного меню.
        Принимает экран (объект Surface), на котором будет отображаться меню.
        """
        self.settings = MemorySettings() # Добавляем настройки
        self.screen = screen  # Сохраняем экран
        self.font = pygame.font.SysFont(None, 48)  # Шрифт для текста кнопок
        # Список кнопок с текстом и соответствующим уровнем сложности
        self.buttons = [
            {"text": "Легкий", "difficulty": "easy"},
            {"text": "Средний", "difficulty": "medium"},
            {"text": "Сложный", "difficulty": "hard"},
            {"text": "Невозможный", "difficulty": "insane"},
            {"text": "Выход", "difficulty": None}  # Кнопка для выхода из игры
        ]

        # Загрузка звуков
        self.button_sound = pygame.mixer.Sound(self.settings.sound_button)
        self.hover_sound_played = False
        self.last_hovered_button = None

    def run(self):
        """
        Основной цикл отображения меню.
        Обрабатывает события и обновляет экран.
        """

        pygame.mixer.music.load(self.settings.sound_background)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Зацикливаем фоновую музыку

        while True:
            self.screen.fill(self.settings.bg_color)  # Заливаем экран тёмно-синим цветом
            self._draw_buttons()  # Рисуем кнопки

            mouse_pos = pygame.mouse.get_pos()
            self._handle_hover(mouse_pos)

            # Обрабатываем события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                    return  # Выход из меню
                if event.type == pygame.MOUSEBUTTONDOWN:  # Клик мыши
                    self._handle_click(*event.pos)  # Обработка клика по кнопке

            pygame.display.flip()  # Обновляем экран

    def _handle_hover(self, mouse_pos):
        """Обработка наведения на кнопки со звуковым эффектом"""
        hovered_button = None
        for btn in self.buttons:
            if btn.get("rect") and btn["rect"].collidepoint(mouse_pos):
                hovered_button = btn
                break

        if hovered_button and hovered_button != self.last_hovered_button:
            if not self.hover_sound_played:
                self.button_sound.play()
                self.hover_sound_played = True
        else:
            self.hover_sound_played = False

        self.last_hovered_button = hovered_button

    def _draw_buttons(self):
        """
        Рисует все кнопки на экране и сохраняет их позиции.
        """
        center_x = self.screen.get_rect().centerx  # Центр экрана по оси X
        mouse_pos = pygame.mouse.get_pos() # Центр экрана по оси Y

        for i, btn in enumerate(self.buttons):
            color = (255, 255, 255)  # Белый цвет по умолчанию

            # Если курсор над кнопкой - меняем цвет
            if btn.get("rect") and btn["rect"].collidepoint(mouse_pos):
                color = (255, 255, 0)  # Желтый цвет при наведении

            # Создаем текст кнопки
            text = self.font.render(btn["text"], True, color)
            # Получаем прямоугольник текста и выравниваем по центру
            rect = text.get_rect(center=(center_x, 200 + i * 80))
            self.screen.blit(text, rect)  # Отображаем текст на экране
            btn["rect"] = rect  # Сохраняем прямоугольник для обработки кликов

    def _handle_click(self, x, y):
        """
        Проверяет, нажал ли пользователь на какую-либо кнопку.
        Если нажал — выполняет соответствующее действие.
        """
        for btn in self.buttons:
            # Проверяем, существует ли прямоугольник и попадает ли в него курсор
            if btn.get("rect") and btn["rect"].collidepoint(x, y):
                self.button_sound.play()  # Звук при нажатии
                if btn["difficulty"]:  # Если это не кнопка "Выход"
                    start_memory_game(self.screen, btn["difficulty"])
                else:
                    pygame.quit()  # Закрываем Pygame
                    exit()  # Выходим из программы
