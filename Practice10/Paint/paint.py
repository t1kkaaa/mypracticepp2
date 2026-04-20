import pygame
import sys
import math

pygame.init()

# ---------- WINDOW ----------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint with UI Panel")

clock = pygame.time.Clock()

# ---------- SETTINGS ----------
color = (0, 0, 255)
mode = "draw"
radius = 5

start_pos = None
drawing = False

# фон
screen.fill((255, 255, 255))

# шрифт для панели
font = pygame.font.SysFont("Arial", 18)

# ---------- UI PANEL ----------
def draw_ui():
    # нижняя панель
    pygame.draw.rect(screen, (230, 230, 230), (0, 560, 800, 40))

    text = "R=Red | G=Green | B=Blue | D=Draw | E=Erase | L=Rect | C=Circle"
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (10, 570))

# ---------- MAIN LOOP ----------
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- KEYBOARD ----------
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                color = (255, 0, 0)

            elif event.key == pygame.K_g:
                color = (0, 255, 0)

            elif event.key == pygame.K_b:
                color = (0, 0, 255)

            elif event.key == pygame.K_d:
                mode = "draw"

            elif event.key == pygame.K_e:
                mode = "erase"

            elif event.key == pygame.K_l:
                mode = "rect"

            elif event.key == pygame.K_c:
                mode = "circle"

        # ---------- MOUSE ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # ---------- RECTANGLE ----------
            if mode == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])

                pygame.draw.rect(screen, color, (x, y, w, h), 2)

            # ---------- CIRCLE ----------
            elif mode == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                radius_circle = int(math.sqrt(dx*dx + dy*dy))

                pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

        # ---------- DRAW / ERASE ----------
        if event.type == pygame.MOUSEMOTION and drawing:

            if mode == "draw":
                pygame.draw.circle(screen, color, event.pos, radius)

            elif mode == "erase":
                pygame.draw.circle(screen, (255, 255, 255), event.pos, 15)

    # ---------- UI ----------
    draw_ui()

    pygame.display.update()
    clock.tick(60)