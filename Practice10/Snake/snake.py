import pygame
import random
import sys

# Инициализация
pygame.init()

# Размеры окна
WIDTH = 600
HEIGHT = 400
CELL = 20

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")


clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont("Verdana", 20)

# ---------- НАСТРОЙКИ ----------
speed = 5
level = 1
score = 0

# Змейка (список координат)
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

# ---------- ГЕНЕРАЦИЯ ЕДЫ ----------
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        # Проверяем чтобы не появлялась на змейке
        if (x, y) not in snake:
            return (x, y)

food = generate_food()

# ---------- ИГРОВОЙ ЦИКЛ ----------
while True:

    # --- события ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # --- движение головы ---
    head_x, head_y = snake[0]

    if direction == "UP":
        head_y -= CELL
    if direction == "DOWN":
        head_y += CELL
    if direction == "LEFT":
        head_x -= CELL
    if direction == "RIGHT":
        head_x += CELL

    new_head = (head_x, head_y)

    # ---------- ПРОВЕРКА СТОЛКНОВЕНИЯ С ГРАНИЦАМИ ----------
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        break  # game over

    # ---------- ПРОВЕРКА СТОЛКНОВЕНИЯ С СОБОЙ ----------
    if new_head in snake:
        break

    snake.insert(0, new_head)

    # ---------- ПРОВЕРКА ЕДЫ ----------
    if new_head == food:
        score += 1
        food = generate_food()  # новая еда

        # ---------- УРОВНИ ----------
        if score % 3 == 0:   # каждые 3 очка
            level += 1
            speed += 2       # увеличиваем скорость

    else:
        snake.pop()  # удаляем хвост если не съели еду

    # ---------- ОТРИСОВКА ----------
    screen.fill(BLACK)

    # змейка
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL, CELL))

    # еда
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # ---------- СЧЁТ И УРОВЕНЬ ----------
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    pygame.display.update()

    clock.tick(speed)

# ---------- GAME OVER ----------
screen.fill(RED)
game_over_text = font.render("GAME OVER", True, WHITE)
screen.blit(game_over_text, (250, 180))
pygame.display.update()
pygame.time.delay(2000)

pygame.quit()
sys.exit()