import pygame
import sys
import math

pygame.init()

# ---------- ОКНО ----------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint")

clock = pygame.time.Clock()

# ---------- НАСТРОЙКИ ----------
color = (0, 0, 255)
mode = "draw"   # режимы: draw, square, rtriangle, etriangle, rhombus
radius = 5

start_pos = None
drawing = False

# фон
screen.fill((255, 255, 255))

# шрифт
font = pygame.font.SysFont("Arial", 16)

# ---------- ФУНКЦИЯ UI ----------
def draw_ui():
    pygame.draw.rect(screen, (230, 230, 230), (0, 560, 800, 40))
    text = "R/G/B=Color | D=Draw | S=Square | T=Right Triangle | E=Equilateral | H=Rhombus"
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (10, 570))

# ---------- MAIN LOOP ----------
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- КЛАВИАТУРА ----------
        if event.type == pygame.KEYDOWN:

            # смена цвета
            if event.key == pygame.K_r:
                color = (255, 0, 0)
            elif event.key == pygame.K_g:
                color = (0, 255, 0)
            elif event.key == pygame.K_b:
                color = (0, 0, 255)

            # режимы
            elif event.key == pygame.K_d:
                mode = "draw"
            elif event.key == pygame.K_s:
                mode = "square"
            elif event.key == pygame.K_t:
                mode = "rtriangle"
            elif event.key == pygame.K_e:
                mode = "etriangle"
            elif event.key == pygame.K_h:
                mode = "rhombus"

        # ---------- МЫШЬ ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            # ---------- КВАДРАТ ----------
            if mode == "square":
                size = min(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, (x1, y1, size, size), 2)

            # ---------- ПРЯМОУГОЛЬНЫЙ ТРЕУГОЛЬНИК ----------
            elif mode == "rtriangle":
                points = [(x1, y1), (x2, y2), (x1, y2)]
                pygame.draw.polygon(screen, color, points, 2)

            # ---------- РАВНОСТОРОННИЙ ТРЕУГОЛЬНИК ----------
            elif mode == "etriangle":
                side = abs(x2 - x1)
                height = int((math.sqrt(3) / 2) * side)

                p1 = (x1, y1)
                p2 = (x1 + side, y1)
                p3 = (x1 + side // 2, y1 - height)

                pygame.draw.polygon(screen, color, [p1, p2, p3], 2)

            # ---------- РОМБ ----------
            elif mode == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2

                points = [
                    (cx, cy - dy),
                    (cx + dx, cy),
                    (cx, cy + dy),
                    (cx - dx, cy)
                ]

                pygame.draw.polygon(screen, color, points, 2)

        # ---------- РИСОВАНИЕ ----------
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "draw":
                pygame.draw.circle(screen, color, event.pos, radius)

    # ---------- UI ----------
    draw_ui()

    pygame.display.update()
    clock.tick(60)