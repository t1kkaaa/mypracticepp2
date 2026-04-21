import pygame, sys
from pygame.locals import *
import random

# ---------- ИНИЦИАЛИЗАЦИЯ ----------
pygame.init()

# FPS
FPS = 60
clock = pygame.time.Clock()

# Размер экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Скорость врага (будет увеличиваться)
SPEED = 5

# Счёт монет
COINS = 0

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифты
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

# Окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Фон
background = pygame.image.load("Images/AnimatedStreet.png")

# ---------- КЛАСС ВРАГА ----------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Enemy.png")
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        # случайная позиция сверху
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        # движение вниз
        self.rect.move_ip(0, SPEED)

        # если вышел за экран — появляется снова
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

# ---------- КЛАСС ИГРОКА ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        pressed = pygame.key.get_pressed()

        # движение влево
        if pressed[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        # движение вправо
        if pressed[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

# ---------- КЛАСС МОНЕТЫ ----------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # загружаем и уменьшаем монету
        img = pygame.image.load("Images/coin.png")
        self.image = pygame.transform.scale(img, (30, 30))

        self.rect = self.image.get_rect()

        # значение монеты (разный "вес")
        self.value = random.choice([1, 3, 5])

        self.reset()

    def reset(self):
        # новая случайная позиция
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

        # каждый раз случайное значение
        self.value = random.choice([1, 3, 5])

    def move(self):
        # монета движется вниз
        self.rect.move_ip(0, SPEED - 2)

        # если ушла за экран
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

# ---------- СОЗДАНИЕ ОБЪЕКТОВ ----------
P1 = Player()
E1 = Enemy()

# создаём несколько монет
coins = pygame.sprite.Group()
for i in range(3):
    coins.add(Coin())

# группы
enemies = pygame.sprite.Group(E1)
all_sprites = pygame.sprite.Group(P1, E1, *coins)

# ---------- ИГРОВОЙ ЦИКЛ ----------
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # фон
    screen.blit(background, (0, 0))

    # движение и отрисовка
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # ---------- СБОР МОНЕТ ----------
    collected = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collected:
        COINS += coin.value   # добавляем значение монеты
        coin.reset()          # создаём новую

    # ---------- УВЕЛИЧЕНИЕ СКОРОСТИ ----------
    # чем больше монет — тем быстрее враг
    if COINS >= 20:
        SPEED = 8
    elif COINS >= 10:
        SPEED = 6
    elif COINS >= 5:
        SPEED = 4

    # ---------- СТОЛКНОВЕНИЕ ----------
    if pygame.sprite.spritecollideany(P1, enemies):
        screen.fill((255, 0, 0))
        text = font_big.render("GAME OVER", True, BLACK)
        screen.blit(text, (50, 250))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # ---------- ВЫВОД СЧЁТА ----------
    text = font_small.render("Coins: " + str(COINS), True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)