import pygame
import time


class MickeysClock:
    def __init__(self, screen, center, hand_image_path):
        self.screen = screen
        self.center = center

        # Загружаем изображение
        self.base_hand = pygame.image.load(hand_image_path).convert_alpha()

        # Шрифты
        self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 24)

        # Цвета
        self.text_color = (214, 51, 108)
        self.label_color = (186, 85, 211)
        self.center_dot_color = (255, 105, 180)

    # 🔥 ИСПРАВЛЕНО (убрали +90)
    def _get_rotation_angle(self, value, max_value):
        return -(value / max_value) * 360

    def blit_rotate(self, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=rotated_center)

        self.screen.blit(rotated_image, rotated_rect)

    def draw(self):
        now = time.localtime()
        minutes = now.tm_min
        seconds = now.tm_sec

        min_angle = self._get_rotation_angle(minutes, 60)
        sec_angle = self._get_rotation_angle(seconds, 60)

        # Размеры рук
        minute_hand = pygame.transform.smoothscale(self.base_hand, (100, 200))
        second_hand = pygame.transform.smoothscale(self.base_hand, (80, 170))

        # Зеркалим вторую руку
        second_hand = pygame.transform.flip(second_hand, True, False)

        # Точка вращения (основание руки)
        pivot_min = (minute_hand.get_width() // 2, minute_hand.get_height() - 10)
        pivot_sec = (second_hand.get_width() // 2, second_hand.get_height() - 10)

        # Рисуем руки
        self.blit_rotate(minute_hand, self.center, pivot_min, min_angle)
        self.blit_rotate(second_hand, self.center, pivot_sec, sec_angle)

        # Центральная точка
        pygame.draw.circle(self.screen, self.center_dot_color, self.center, 7)

        # Цифровое время
        time_str = time.strftime("%M:%S", now)
        text_surf = self.font_large.render(time_str, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.center[0], self.center[1] - 230))
        self.screen.blit(text_surf, text_rect)

        # Подписи
        label_min = self.font_small.render("Big hand = minutes", True, self.label_color)
        label_sec = self.font_small.render("Small hand = seconds", True, self.label_color)

        self.screen.blit(label_min, label_min.get_rect(center=(self.center[0], self.center[1] + 220)))
        self.screen.blit(label_sec, label_sec.get_rect(center=(self.center[0], self.center[1] + 250)))