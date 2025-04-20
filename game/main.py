import pygame  # Импортируем библиотеку Pygame для создания графического интерфейса
from game import MemorySettings

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

    def run(self):
        """
        Основной цикл отображения меню.
        Обрабатывает события и обновляет экран.
        """
        while True:
            self.screen.fill(self.settings.bg_color)  # Заливаем экран тёмно-синим цветом
            self._draw_buttons()  # Рисуем кнопки

            # Обрабатываем события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                    return  # Выход из меню
                if event.type == pygame.MOUSEBUTTONDOWN:  # Клик мыши
                    self._handle_click(*event.pos)  # Обработка клика по кнопке

            pygame.display.flip()  # Обновляем экран

    def _draw_buttons(self):
        """
        Рисует все кнопки на экране и сохраняет их позиции.
        """
        center_x = self.screen.get_rect().centerx  # Центр экрана по оси X

        for i, btn in enumerate(self.buttons):
            # Создаем текст кнопки
            text = self.font.render(btn["text"], True, (255, 255, 255))
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
                if btn["difficulty"]:  # Если это не кнопка "Выход"
                    print(btn["difficulty"])  # Печатаем выбранную сложность (для проверки работоспособности программы)
                else:
                    pygame.quit()  # Закрываем Pygame
                    exit()  # Выходим из программы
