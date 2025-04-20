import pygame
from game import MainMenu, MemorySettings

def run_game():
    pygame.init() # инициализация pygame
    settings = MemorySettings() # инициализация настроек
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height)) # настройка окна
    pygame.display.set_caption("Memory Game") # задаем имя окну
    MainMenu(screen).run() # запускаем отображение
    pygame.quit() # выход по окончанию сессии

if __name__ == '__main__':
    """
    проверяет, что игра запускается из этого файла.
    т.е. проверяет, является ли он основным.
    """
    run_game() # запуск игры