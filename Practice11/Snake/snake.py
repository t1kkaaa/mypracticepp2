import pygame
import random
import sys
import time

pygame.init()

# ---------- НАСТРОЙКИ ----------
WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Advanced")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Шрифт
font = pygame.font.SysFont("Verdana", 20)

# ---------- ИГРОВЫЕ ПЕРЕМЕННЫЕ ----------
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

score = 0
speed = 7

# ---------- ФУНКЦИЯ СОЗДАНИЯ ЕДЫ ----------
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        # вес еды (разные очки)
        weight = random.choice([1, 3, 5])

        # проверка чтобы не появлялась на змейке
        if (x, y) not in snake:
            return {"pos": (x, y), "weight": weight, "time": time.time()}

food = generate_food()

# сколько секунд живёт еда
FOOD_LIFETIME = 5

# ---------- ИГРОВОЙ ЦИКЛ ----------
while True:

    # ---------- СОБЫТИЯ ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # ---------- ДВИЖЕНИЕ ----------
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

    # ---------- ПРОВЕРКА СТОЛКНОВЕНИЙ ----------
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        break

    if new_head in snake:
        break

    snake.insert(0, new_head)

    # ---------- ПРОВЕРКА ЕДЫ ----------
    if new_head == food["pos"]:
        score += food["weight"]  # добавляем вес еды
        food = generate_food()   # создаём новую еду
    else:
        snake.pop()

    # ---------- ТАЙМЕР ЕДЫ ----------
    # если прошло больше 5 секунд — еда исчезает
    if time.time() - food["time"] > FOOD_LIFETIME:
        food = generate_food()

    # ---------- ОТРИСОВКА ----------
    screen.fill(BLACK)

    # змейка
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL, CELL))

    # еда (цвет зависит от веса)
    if food["weight"] == 1:
        color = RED
    elif food["weight"] == 3:
        color = YELLOW
    else:
        color = WHITE

    pygame.draw.rect(screen, color, (food["pos"][0], food["pos"][1], CELL, CELL))

    # ---------- ТЕКСТ ----------
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(speed)

# ---------- GAME OVER ----------
screen.fill(RED)
text = font.render("GAME OVER", True, WHITE)
screen.blit(text, (250, 180))
pygame.display.update()
pygame.time.delay(2000)

pygame.quit()
sys.exit()