import pygame
import time
from game import MemorySettings  # Импорт класса с настройками игры
from game.memory_objects.game_screen import GameScreen  # Импорт игрового экрана

def start_memory_game(screen, difficulty):
    """
    Запускает основную игровую петлю для игры на память.

    :param screen: Поверхность Pygame, на которой происходит отрисовка.
    :param difficulty: Уровень сложности игры (easy, medium, hard, insane).
    """
    settings = MemorySettings(difficulty)  # Создаем объект с настройками игры на основе выбранной сложности
    game = GameScreen(screen, settings)    # Создаем игровой экран, передаём ему настройки и экран
    start_time = time.time()               # Сохраняем момент начала игры

    while True:
        # Вычисляем прошедшее время и оставшееся (в секундах)
        elapsed = time.time() - start_time
        remaining = max(settings.time_limit - int(elapsed), 0)  # Не допускаем отрицательного времени

        # Обрабатываем все события (нажатия, закрытие окна и т.д.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return  # Выход из игры при закрытии окна или нажатии ESC
            game.handle_event(event)  # Передаём событие в игровой экран для обработки

        # Обновляем состояние игры (например, проверка пар и времени)
        game.update(remaining)

        # Рисуем текущее состояние игры на экран
        game.draw()

        # Обновляем окно
        pygame.display.flip()

        # Проверка завершения игры
        if game.is_game_over():
            if game.game_over_type == "back":  # Если игрок нажал "Назад", просто выходим
                return
            game.show_stats_screen(int(elapsed))  # Показываем статистику после победы/поражения
            return
