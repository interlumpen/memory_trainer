import pygame  # Импортируем библиотеку Pygame для создания графического интерфейса
import time    # Импортируем модуль time для отслеживания времени

def show_stats_screen(screen, score, result, moves, time_used):
    """
    Показывает экран с результатами после окончания игры.

    :param screen: Поверхность Pygame для отображения.
    :param score: Финальный счет игрока.
    :param result: Строка с результатом игры (например, "Победа" или "Поражение").
    :param moves: Количество ходов, сделанных игроком.
    :param time_used: Время, затраченное на игру (в секундах).
    """

    # Создаем список шрифтов разного размера для каждой строки статистики
    fonts = [pygame.font.SysFont(None, size) for size in [72, 44, 44, 44, 44]]

    clock = pygame.time.Clock()  # Создаем объект Clock для контроля FPS
    start = time.time()  # Засекаем начальное время отображения экрана

    while True:
        screen.fill((20, 20, 50))  # Заливаем экран темно-синим цветом

        # Вычисляем прогресс анимации появления очков (от 0 до 1 за 2 секунды)
        progress = min(1.0, (time.time() - start) / 2)

        # Формируем список строк для отображения
        lines = [
            f"{result}",                             # Результат (Победа / Поражение)
            f"Ходов: {moves}",                       # Количество ходов
            f"Время: {time_used} сек",               # Время в секундах
            f"Очки: {int(score * progress)}",        # Плавная анимация увеличения очков
            "Нажмите любую клавишу для выхода"       # Подсказка пользователю
        ]

        # Отображаем все строки на экране по центру
        for i, (line, font) in enumerate(zip(lines, fonts)):
            text = font.render(line, True, (255, 255, 255))  # Рендерим текст
            # Центрируем текст по горизонтали, вертикальное положение зависит от индекса
            screen.blit(text, text.get_rect(center=(screen.get_width() // 2, 150 + i * 60)))

        pygame.display.flip()  # Обновляем экран

        # Обработка событий
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return  # Выходим из экрана статистики при любом действии пользователя

        clock.tick(60)  # Ограничиваем частоту обновления до 60 кадров в секунду
