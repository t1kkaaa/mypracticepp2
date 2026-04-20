import pygame, sys
from pygame.locals import *
import random, time

# Инициализация всех модулей Pygame
pygame.init()

# ---------- НАСТРОЙКИ ВРЕМЕНИ ----------
FPS = 60
FramePerSec = pygame.time.Clock()

# ---------- ЦВЕТА (RGB) ----------
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ---------- ПАРАМЕТРЫ ЭКРАНА ----------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Игровые переменные
SPEED = 5   # Начальная скорость врагов
SCORE = 0   # Очки (за пропущенные машины)
COINS = 0   # Количество собранных монет

# ---------- ШРИФТЫ И ТЕКСТ ----------
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
# Заранее создаем поверхность с текстом "Game Over"
game_over = font.render("Game Over", True, BLACK)

# Загрузка фонового изображения (дороги)
background = pygame.image.load("Images/AnimatedStreet.png")

# Создание игрового окна
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
        """Возвращает врага в начало пути в случайную позицию по горизонтали"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        # Движение вниз по оси Y
        self.rect.move_ip(0, SPEED)
        # Если враг уехал за нижнюю границу экрана
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1   # Увеличиваем счет
            self.reset() # Перемещаем врага наверх

# ---------- КЛАСС ИГРОКА ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Images/Player.png")
        self.rect = self.image.get_rect()
        # Начальная позиция игрока
        self.rect.center = (160, 520)

    def move(self):
        """Обработка управления клавишами 'Влево' и 'Вправо'"""
        pressed_keys = pygame.key.get_pressed()
        
        # Движение влево с ограничением по краю экрана
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        
        # Движение вправо с ограничением по краю экрана
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# ---------- КЛАСС МОНЕТЫ ----------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Загрузка и изменение размера изображения монеты
        original_image = pygame.image.load("Images/Coin.png")
        self.image = pygame.transform.scale(original_image, (40, 40))
        
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        """Появление монеты в случайном месте сверху"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        # Монеты двигаются чуть медленнее машин
        self.rect.move_ip(0, SPEED - 2)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

# ---------- СОЗДАНИЕ ОБЪЕКТОВ ----------
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группировка спрайтов для удобства обработки
enemies = pygame.sprite.Group()
enemies.add(E1)

Coins = pygame.sprite.Group()
Coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# ---------- ПОЛЬЗОВАТЕЛЬСКИЕ СОБЫТИЯ ----------
# Событие для постепенного увеличения скорости игры
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000) # Срабатывает каждую секунду

# ---------- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ----------
while True:

    # Обработка событий
    for event in pygame.event.get():
        # Увеличение общей скорости
        if event.type == INC_SPEED:
            SPEED += 0.5

        # Выход из игры
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение счета очков (слева сверху)
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    # Отображение собранных монет (справа сверху)
    Coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(Coin_text, (280, 10))

    # Обновление позиций и отрисовка всех объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # ---------- ОБРАБОТКА КОЛЛИЗИЙ (СТОЛКНОВЕНИЙ) ----------
    
    # Сбор монет: проверяем столкновение Игрока и группы Монет
    collected = pygame.sprite.spritecollide(P1, Coins, False)
    if collected:
        COINS += 1
        for coin in collected:
            coin.reset() # При сборе монета исчезает и появляется сверху

    # Столкновение с врагом: проверяем столкновение Игрока и группы Врагов
    if pygame.sprite.spritecollideany(P1, enemies):
        # Звук аварии
        pygame.mixer.Sound("Sounds/crash.wav").play()
        time.sleep(0.5)

        # Экран Game Over
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        
        # Пауза перед закрытием
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Обновление экрана
    pygame.display.update()
    # Поддержание стабильного FPS
    FramePerSec.tick(FPS)