import pygame
import random
import sys

# Инициализация библиотеки Pygame
pygame.init()

# ---------- НАСТРОЙКИ ОКНА ----------
WIDTH = 600      # Ширина экрана
HEIGHT = 400     # Высота экрана
CELL = 20        # Размер одной ячейки (сетки)

# Цвета (RGB)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Создание окна и установка заголовка
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Объект для контроля времени (FPS)
clock = pygame.time.Clock()

# Шрифт для текста
font = pygame.font.SysFont("Verdana", 20)

# ---------- ИГРОВЫЕ ПАРАМЕТРЫ ----------
speed = 5        # Начальная скорость (кадры в секунду)
level = 1        # Текущий уровень
score = 0        # Набранные очки

# Змейка представлена списком кортежей (координат). 
# Первый элемент — голова, остальные — сегменты тела.
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT" # Начальное направление движения

# ---------- ФУНКЦИЯ ГЕНЕРАЦИИ ЕДЫ ----------
def generate_food():
    """Создает координаты еды, выровненные по сетке, вне тела змейки"""
    while True:
        # Генерируем случайное число кратное размеру ячейки (CELL)
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        # Проверяем, чтобы еда не появилась внутри змейки
        if (x, y) not in snake:
            return (x, y)

# Создаем первую порцию еды
food = generate_food()

# ---------- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ----------
while True:

    # --- 1. ОБРАБОТКА СОБЫТИЙ ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Управление направлением (с защитой от разворота на 180 градусов)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # --- 2. ЛОГИКА ДВИЖЕНИЯ ---
    # Получаем текущие координаты головы
    head_x, head_y = snake[0]

    # Вычисляем новые координаты головы в зависимости от направления
    if direction == "UP":
        head_y -= CELL
    if direction == "DOWN":
        head_y += CELL
    if direction == "LEFT":
        head_x -= CELL
    if direction == "RIGHT":
        head_x += CELL

    new_head = (head_x, head_y)

    # --- 3. ПРОВЕРКА СТОЛКНОВЕНИЙ ---
    # Проверка выхода за границы экрана
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        break  # Выход из цикла (Game Over)

    # Проверка столкновения с собственным телом
    if new_head in snake:
        break # Выход из цикла (Game Over)

    # Добавляем новую голову в начало списка
    snake.insert(0, new_head)

    # --- 4. ПРОВЕРКА ПОЕДАНИЯ ЕДЫ ---
    if new_head == food:
        score += 1
        food = generate_food()  # Создаем новую еду

        # Система уровней
        if score % 3 == 0:   # Каждые 3 съеденные единицы еды
            level += 1
            speed += 2       # Увеличиваем скорость (сложность)
    else:
        # Если еду не съели, удаляем последний сегмент хвоста.
        # Это создает эффект движения: голова добавилась, хвост убрался.
        snake.pop()

    # --- 5. ОТРИСОВКА ---
    screen.fill(BLACK) # Очистка экрана черным цветом

    # Рисуем каждый сегмент змейки
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL, CELL))

    # Рисуем еду
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Отображаем счет и уровень в углу экрана
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    # Обновляем дисплей
    pygame.display.update()

    # Задаем скорость игры
    clock.tick(speed)

# ---------- ЭКРАН ЗАВЕРШЕНИЯ ИГРЫ (GAME OVER) ----------
screen.fill(RED)
game_over_text = font.render("GAME OVER", True, WHITE)
# Рисуем текст примерно по центру
screen.blit(game_over_text, (WIDTH // 2 - 60, HEIGHT // 2 - 20))
pygame.display.update()

# Пауза 2 секунды перед закрытием
pygame.time.delay(2000)

pygame.quit()
sys.exit()