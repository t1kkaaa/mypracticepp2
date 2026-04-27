import pygame

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (210, 210, 210)
DARK_GRAY = (150, 150, 150)
RED = (220, 60, 60)
GREEN = (60, 170, 90)
BLUE = (70, 120, 220)


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface, font, mouse_pos):
        color = DARK_GRAY if self.rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def draw_center_text(surface, text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(text_surface, text_rect)


def draw_left_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))