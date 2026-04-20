import pygame, sys
from pygame.locals import *
import random, time

# Инициализация
pygame.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размер экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Скорость и очки
SPEED = 5
SCORE = 0
COINS = 0

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Фон
background = pygame.image.load("Images/AnimatedStreet.png")

# Окно
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

# ---------- КЛАСС ВРАГА ----------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Enemy.png")
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset()

# ---------- КЛАСС ИГРОКА ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # загружаем изображение
        original_image = pygame.image.load("Images/Coin.png")
        
        # уменьшаем (ширина, высота)
        self.image = pygame.transform.scale(original_image, (40, 40))
        
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED - 2)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы
enemies = pygame.sprite.Group()
enemies.add(E1)

Coins = pygame.sprite.Group()
Coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Увеличение скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# ---------- ИГРОВОЙ ЦИКЛ ----------
while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Фон
    DISPLAYSURF.blit(background, (0, 0))

    # Счёт
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    # Монеты (справа)
    Coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(Coin_text, (280, 10))

    # Движение и отрисовка
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Сбор монет
    collected = pygame.sprite.spritecollide(P1, Coins, False)
    if collected:
        COINS += 1
        for Coin in collected:
            Coin.reset()

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("Sounds/crash.wav").play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)