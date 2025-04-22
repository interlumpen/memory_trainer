import pygame  # Импортируем библиотеку Pygame для создания графического интерфейса

class Card:
    def __init__(self, rect, image, id):
        """
        Инициализация карты.

        :param rect: Прямоугольник (pygame.Rect), определяющий позицию и размер карты.
        :param image: Изображение, которое будет показываться при открытии карты.
        :param id: Уникальный идентификатор карты (нужен для проверки совпадений).
        """
        self.rect = rect  # Область, где расположена карта на экране
        self.image = image  # Картинка, скрытая под "рубашкой"
        self.id = id  # ID карты (используется для сравнения при совпадении)
        self.revealed = False  # Показывает ли карта свою картинку (открыта или нет)
        self.matched = False  # Совпала ли карта с другой (найдена пара)
        self.back_color = (100, 100, 200)  # Цвет рубашки карты (задняя сторона)

    def draw(self, screen):
        """
        Отрисовка карты на экране.

        :param screen: Поверхность Pygame, на которую будет рисоваться карта.
        """
        if self.matched:
            return  # Если карта уже угадана, больше не рисуем её

        if self.revealed:
            # Если карта открыта, рисуем картинку
            screen.blit(self.image, self.rect)
        else:
            # Если карта закрыта, рисуем её рубашку
            pygame.draw.rect(screen, self.back_color, self.rect)  # Заливка
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)  # Белая рамка

    def handle_click(self, pos):
        """
        Обработка клика по карте.

        :param pos: Координаты курсора мыши при клике.
        :return: True, если карта была успешно открыта; иначе False.
        """
        if (
            self.rect.collidepoint(pos)  # Клик попал внутрь карты
            and not self.revealed         # Карта еще не была открыта
            and not self.matched          # И не совпала ранее
        ):
            self.revealed = True  # Открываем карту
            return True
        return False  # Ничего не произошло

    def hide(self):
        """
        Закрывает карту, если она не была угадана.
        """
        if not self.matched:
            self.revealed = False  # Закрываем изображение

    def mark_matched(self):
        """
        Помечает карту как угаданную (совпавшую с другой).
        """
        self.matched = True
