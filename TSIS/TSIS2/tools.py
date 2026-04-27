import math
from collections import deque
import pygame


def draw_line(surface, color, start, end, width):
    pygame.draw.line(surface, color, start, end, width)


def get_rect_data(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    return x, y, w, h


def draw_rectangle(surface, color, start_pos, end_pos, width):
    x, y, w, h = get_rect_data(start_pos, end_pos)
    pygame.draw.rect(surface, color, (x, y, w, h), width)


def draw_circle(surface, color, start_pos, end_pos, width):
    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
    pygame.draw.circle(surface, color, start_pos, radius, width)


def draw_square(surface, color, start_pos, end_pos, width):
    x, y, w, h = get_rect_data(start_pos, end_pos)
    side = min(w, h)
    pygame.draw.rect(surface, color, (x, y, side, side), width)


def draw_right_triangle(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    side = abs(x2 - x1)
    if side == 0:
        return

    height = int((math.sqrt(3) / 2) * side)

    if y2 >= y1:
        p1 = (x1, y1 + height)
        p2 = (x1 + side, y1 + height)
        p3 = (x1 + side // 2, y1)
    else:
        p1 = (x1, y1)
        p2 = (x1 + side, y1)
        p3 = (x1 + side // 2, y1 - height)

    pygame.draw.polygon(surface, color, [p1, p2, p3], width)


def draw_rhombus(surface, color, start_pos, end_pos, width):
    x, y, w, h = get_rect_data(start_pos, end_pos)
    points = [
        (x + w // 2, y),
        (x + w, y + h // 2),
        (x + w // 2, y + h),
        (x, y + h // 2)
    ]
    pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x, y = start_pos

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))
    fill_color_rgba = pygame.Color(*fill_color)

    if target_color == fill_color_rgba:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()

        if not (0 <= cx < width and 0 <= cy < height):
            continue

        if surface.get_at((cx, cy)) != target_color:
            continue

        surface.set_at((cx, cy), fill_color_rgba)

        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))