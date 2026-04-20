import pygame
import sys
import math

# Инициализация всех модулей pygame
pygame.init()

# ---------- НАСТРОЙКИ ОКНА ----------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint with UI Panel")

# Объект для контроля частоты кадров (FPS)
clock = pygame.time.Clock()

# ---------- ПАРАМЕТРЫ КИСТИ И СОСТОЯНИЯ ----------
color = (0, 0, 255)      # Текущий цвет (по умолчанию синий)
mode = "draw"            # Текущий режим: draw, erase, rect, circle
radius = 5               # Радиус кисти для рисования

start_pos = None         # Точка начала нажатия мыши (для фигур)
drawing = False          # Флаг: зажата ли кнопка мыши

# Заливка начального фона белым цветом
screen.fill((255, 255, 255))

# Настройка шрифта для отображения подсказок в UI
font = pygame.font.SysFont("Arial", 18)

# ---------- ФУНКЦИЯ ИНТЕРФЕЙСА (UI) ----------
def draw_ui():
    """Рисует панель инструментов в нижней части экрана"""
    # Рисуем серый прямоугольник внизу окна
    pygame.draw.rect(screen, (230, 230, 230), (0, 560, 800, 40))

    # Текст с подсказками по горячим клавишам
    text = "R=Red | G=Green | B=Blue | D=Draw | E=Erase | L=Rect | C=Circle"
    img = font.render(text, True, (0, 0, 0))
    # Выводим текст поверх панели
    screen.blit(img, (10, 570))

# ---------- ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ ----------
while True:

    # Обработка событий (очередь событий от системы)
    for event in pygame.event.get():

        # Закрытие окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- ОБРАБОТКА КЛАВИАТУРЫ ----------
        if event.type == pygame.KEYDOWN:
            # Смена цвета
            if event.key == pygame.K_r:
                color = (255, 0, 0)   # Красный
            elif event.key == pygame.K_g:
                color = (0, 255, 0)   # Зеленый
            elif event.key == pygame.K_b:
                color = (0, 0, 255)   # Синий
            
            # Смена режима инструмента
            elif event.key == pygame.K_d:
                mode = "draw"         # Рисование
            elif event.key == pygame.K_e:
                mode = "erase"        # Ластик
            elif event.key == pygame.K_l:
                mode = "rect"         # Прямоугольник
            elif event.key == pygame.K_c:
                mode = "circle"       # Круг

        # ---------- ОБРАБОТКА МЫШИ ----------
        # Нажатие кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos  # Запоминаем координаты начала (для фигур)

        # Отпускание кнопки мыши
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos    # Конечные координаты

            # РИСОВАНИЕ ПРЯМОУГОЛЬНИКА (при отпускании мыши)
            if mode == "rect":
                # Находим верхний левый угол (минимум координат)
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                # Вычисляем ширину и высоту
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])
                # Рисуем контур прямоугольника (толщина линии 2)
                pygame.draw.rect(screen, color, (x, y, w, h), 2)

            # РИСОВАНИЕ КРУГА (при отпускании мыши)
            elif mode == "circle":
                # Вычисляем расстояние между началом и концом по теореме Пифагора
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                radius_circle = int(math.sqrt(dx*dx + dy*dy))
                # Рисуем круг с центром в точке нажатия
                pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

        # ДВИЖЕНИЕ МЫШИ (для рисования линий)
        if event.type == pygame.MOUSEMOTION and drawing:
            # Свободное рисование (рисуем маленькие круги при движении)
            if mode == "draw":
                pygame.draw.circle(screen, color, event.pos, radius)

            # Ластик (рисуем большие белые круги)
            elif mode == "erase":
                pygame.draw.circle(screen, (255, 255, 255), event.pos, 15)

    # ---------- ОБНОВЛЕНИЕ ЭКРАНА ----------
    # Перерисовываем UI поверх нарисованного
    draw_ui()

    # Обновляем содержимое всего дисплея
    pygame.display.update()
    
    # Ограничение до 60 кадров в секунду
    clock.tick(60)