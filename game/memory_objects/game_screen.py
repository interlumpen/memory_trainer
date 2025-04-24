import pygame
import random
import time
from game.memory_objects.card import Card  # Класс карты
from game.memory_objects.stats_screen import show_stats_screen  # Функция для отображения экрана результатов

class GameScreen:
    def __init__(self, screen, settings):
        """
        Инициализация игрового экрана.

        :param screen: Поверхность Pygame для отображения.
        :param settings: Объект с настройками игры (размер поля, лимиты и т.д.).
        """
        self.screen = screen
        self.settings = settings
        self.cards = []  # Все карточки
        self.first_card = None  # Первая выбранная карта
        self.second_card = None  # Вторая выбранная карта
        self.last_flip_time = 0  # Время последнего переворота
        self.moves = 0  # Количество сделанных ходов
        self.font = pygame.font.SysFont(None, 36)  # Шрифт для текстовой информации
        self.remaining_time = settings.time_limit  # Остаток времени
        self.remaining_moves = settings.max_moves  # Остаток ходов
        self.game_over_type = None  # Статус завершения игры ("Победа", "Проигрыш", "back")
        self.score = 0  # Очки игрока
        self.match_timer = 0  # Таймер для задержки исчезновения совпавших карт
        self.matched_pairs = []  # Список для хранения совпавших пар
        self.showing_match = False  # Флаг отображения совпадения
        self.match_display_time = 0  # Время отображения совпадения
        self.back_button_rect = pygame.Rect(20, 20, 100, 40)  # Кнопка "Назад"

        # Загрузка звуков
        self.sounds = {
            'flip': pygame.mixer.Sound(self.settings.sound_flip),
            'match': pygame.mixer.Sound(self.settings.sound_match),
            'mismatch': pygame.mixer.Sound(self.settings.sound_mismatch),
            'win': pygame.mixer.Sound(self.settings.sound_win),
            'lose': pygame.mixer.Sound(self.settings.sound_lose),
            'button': pygame.mixer.Sound(self.settings.sound_button)
        }

        # Анимационные переменные
        self.message_alpha = 0
        self.message_text = ""
        self.message_timer = 0

        self._generate_cards()  # Генерация игрового поля

    def play_sound(self, sound_name):
        """Воспроизводит звуковой эффект"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def show_message(self, text, duration):
        """Показывает временное сообщение на экране"""
        self.message_text = text
        self.message_alpha = 3000
        self.message_timer = time.time() + duration

    def _generate_cards(self):
        """
        Создание и размещение карточек на игровом поле.
        """
        images = self._load_images(self.settings.total_cards // 2)  # Генерируем половину пар
        images *= 2  # Дублируем для пар
        random.shuffle(images)  # Перемешиваем

        margin = 10
        card_width = 75
        card_height = 75
        top_offset = 100

        # Вычисляем отступы для центрирования
        spacing_x = (self.settings.screen_width - (self.settings.cols * (card_width + margin))) // 2
        spacing_y = ((self.settings.screen_height - top_offset) - (self.settings.rows * (card_height + margin))) // 2 + top_offset

        self.cards = []

        # Создание карточек в сетке
        for row in range(self.settings.rows):
            for col in range(self.settings.cols):
                x = spacing_x + col * (card_width + margin)
                y = spacing_y + row * (card_height + margin)
                rect = pygame.Rect(x, y, card_width, card_height)
                image = images.pop()
                card = Card(rect, image, id=image)  # Создаем объект карты
                self.cards.append(card)

    def _load_images(self, count):
        """
        Создает изображения для карт.

        :param count: Количество уникальных изображений.
        """
        images = []
        for i in range(count):
            surface = pygame.Surface((75, 75))
            surface.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))  # Случайный цвет
            images.append(surface)
        return images

    def handle_event(self, event):
        """
        Обработка пользовательских событий: клики мыши, нажатие на кнопку "Назад".

        :param event: Событие Pygame.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия на кнопку "Назад"
            if self.back_button_rect.collidepoint(event.pos):
                self.play_sound('button')
                self.game_over_type = "back"
                return

        # Если игра завершена — ничего не делаем
        if self.game_over_type:
            return

        if self.showing_match or self.game_over_type:
            return

        # Обработка клика по карточке
        if (event.type == pygame.MOUSEBUTTONDOWN and not self.second_card and
                self.remaining_moves > 0):
            pos = pygame.mouse.get_pos()
            for card in self.cards:
                if card.handle_click(pos) and card not in [c for pair in self.matched_pairs for c in pair]:
                    self.play_sound('flip')
                    if not self.first_card:
                        self.first_card = card
                    elif card != self.first_card:
                        self.second_card = card
                        self.moves += 1
                        self.remaining_moves -= 1
                        self.last_flip_time = time.time()

    def update(self, remaining_time):
        """
        Логика игры: обработка совпадений, проверка условий завершения.

        :param remaining_time: Обновленное время (снаружи).
        """
        self.remaining_time = remaining_time

        # Обновление анимации всех карт
        for card in self.cards:
            card.update_animation()

        # Обновление анимации сообщения
        if self.message_alpha > 0 and time.time() < self.message_timer:
            self.message_alpha -= 1
        else:
            self.message_text = ""

        # Обработка совпадения карт
        if (self.first_card and self.second_card and
                not self.first_card.animating and not self.second_card.animating):

            if time.time() - self.last_flip_time > 1:
                if self.first_card.id == self.second_card.id:
                    # Совпадение найдено
                    self.first_card.mark_matched()
                    self.second_card.mark_matched()
                    self.matched_pairs.append((self.first_card, self.second_card))
                    self.play_sound('match')
                    self.show_message("Совпадение!", 1.5)
                    self.showing_match = True
                    self.match_display_time = time.time() + 1
                else:
                    # Не совпало
                    self.first_card.hide()
                    self.second_card.hide()
                    self.play_sound('mismatch')
                    self.show_message("Не совпало!", 1.5)

                self.first_card = None
                self.second_card = None

        # Запуск исчезновения совпавших карт после задержки
        if (self.showing_match and time.time() > self.match_display_time and
                self.matched_pairs):

            for card1, card2 in self.matched_pairs:
                card1.start_fade_out()
                card2.start_fade_out()

            self.matched_pairs = []
            self.showing_match = False

        # Проверка на победу (все карты открыты)
        if all(card.matched for card in self.cards):
            self.game_over_type = "Победа!"
            self.play_sound('win')
            self.calculate_score()
        # Проверка на проигрыш (время или ходы закончились)
        elif self.remaining_time <= 0 or self.remaining_moves <= 0:
            self.game_over_type = "Проигрыш!"
            self.play_sound('lose')
            self.calculate_score(failed=True)

    def calculate_score(self, failed=False):
        """
        Подсчет очков в зависимости от результата и затраченных ресурсов.

        :param failed: Булево значение — проиграл ли игрок.
        """
        base = 10000
        penalty = self.moves * 30 + (self.settings.time_limit - self.remaining_time) * 30
        bonus = (self.remaining_moves * self.remaining_time) * 100
        score = max(0, base - penalty + bonus)
        if failed:
            score = int(score * 0.5)
        self.score = score

    def draw(self):
        """
        Отрисовка всех элементов на экране: карты, счетчики, кнопки.
        """
        self.screen.fill((30, 30, 60))  # Заливка фона

        for card in self.cards:
            card.draw(self.screen)  # Рисуем карты

        # Рисуем временное сообщение
        if self.message_text:
            text_surface = self.font.render(self.message_text, True, (255, 255, 255))
            text_surface.set_alpha(self.message_alpha)
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, 70))
            self.screen.blit(text_surface, text_rect)

        # Отображаем текст с оставшимися ходами и временем
        moves_text = self.font.render(f"Ходы: {self.remaining_moves}", True, (255, 255, 255))
        time_text = self.font.render(f"Время: {self.remaining_time}", True, (255, 255, 255))
        self.screen.blit(moves_text, (150, 30))
        self.screen.blit(time_text, (300, 30))

        # Рисуем кнопку "Назад"
        pygame.draw.rect(self.screen, (200, 50, 50), self.back_button_rect)
        back_text = self.font.render("Назад", True, (255, 255, 255))
        self.screen.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def is_game_over(self):
        """
        Проверяет, завершена ли игра.

        :return: True, если игра окончена.
        """
        return self.game_over_type is not None

    def show_stats_screen(self, time_used):
        """
        Отображает экран статистики после завершения игры.

        :param time_used: Общее время игры.
        """
        show_stats_screen(
            self.screen,
            self.score,
            self.game_over_type,
            self.moves,
            time_used
        )
