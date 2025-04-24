import pygame
import math


class Card:
    def __init__(self, rect, image, id):
        self.rect = rect
        self.image = image
        self.id = id
        self.revealed = False
        self.matched = False
        self.back_color = (100, 100, 200)
        self.animation_angle = 0
        self.animating = False
        self.animation_speed = 0.2
        self.scale = 1.0
        self.pulse_direction = 0.01
        self.fade_alpha = 255  # Прозрачность для эффекта исчезновения
        self.fading = False  # Флаг процесса исчезновения

    def start_flip_animation(self):
        self.animating = True
        self.animation_angle = 0

    def start_fade_out(self):
        """Начинает анимацию исчезновения карты"""
        self.fading = True
        self.fade_alpha = 255

    def update_animation(self):
        if self.animating:
            self.animation_angle += self.animation_speed
            if self.animation_angle >= math.pi / 2:
                self.animating = False
                self.revealed = not self.revealed
                self.animation_angle = 0

        if self.matched and not self.animating:
            # Анимация пульсации для совпавших карт
            self.scale += self.pulse_direction
            if self.scale > 1.1 or self.scale < 0.9:
                self.pulse_direction *= -1

        if self.fading:
            self.fade_alpha -= 5
            if self.fade_alpha <= 0:
                self.fading = False
                self.fade_alpha = 0

    def draw(self, screen):
        if self.fade_alpha == 0:
            return  # Полностью прозрачная карта - не рисуем

        if self.matched and not self.animating and not self.fading:
            # Анимация пульсации для совпавших карт
            scaled_width = int(self.rect.width * self.scale)
            scaled_height = int(self.rect.height * self.scale)
            offset_x = (self.rect.width - scaled_width) // 2
            offset_y = (self.rect.height - scaled_height) // 2

            if self.revealed:
                scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
                if self.fading:
                    scaled_image.set_alpha(self.fade_alpha)
                screen.blit(scaled_image, (self.rect.x + offset_x, self.rect.y + offset_y))
            return

        # Остальная логика отрисовки без изменений
        if self.animating:
            progress = math.sin(self.animation_angle)
            width = max(1, int(self.rect.width * (1 - abs(progress))))
            temp_rect = pygame.Rect(0, 0, width, self.rect.height)
            temp_rect.center = self.rect.center

            if not self.revealed:
                if progress < 0:
                    pygame.draw.rect(screen, self.back_color, temp_rect)
                    pygame.draw.rect(screen, (255, 255, 255), temp_rect, 2)
                else:
                    temp_img = pygame.transform.scale(self.image, (width, self.rect.height))
                    screen.blit(temp_img, temp_rect)
            else:
                if progress < 0:
                    temp_img = pygame.transform.scale(self.image, (width, self.rect.height))
                    screen.blit(temp_img, temp_rect)
                else:
                    pygame.draw.rect(screen, self.back_color, temp_rect)
                    pygame.draw.rect(screen, (255, 255, 255), temp_rect, 2)
        else:
            if self.revealed:
                img = self.image.copy()
                if self.fading:
                    img.set_alpha(self.fade_alpha)
                screen.blit(img, self.rect)
            else:
                back = pygame.Surface((self.rect.width, self.rect.height))
                back.fill(self.back_color)
                if self.fading:
                    back.set_alpha(self.fade_alpha)
                screen.blit(back, self.rect)
                pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def handle_click(self, pos):
        """Обрабатывает клик по карте"""
        if (self.rect.collidepoint(pos) and         # Клик попал внутрь карты
            not self.revealed and                   # Карта еще не была открыта
            not self.matched and                    # И не совпала ранее
            not self.animating and                  # И не в процессе анимации
            self.fade_alpha == 255):                # И не исчезает
            self.start_flip_animation()
            return True
        return False
    def hide(self):
        """Закрывает карту, если она не была угадана"""
        if not self.matched and self.revealed:
            self.start_flip_animation()  # Начинаем анимацию закрытия

    def mark_matched(self):
        """Помечает карту как угаданную"""
        self.matched = True
