import pygame
import sys
from datetime import datetime

from tools import (
    draw_line,
    draw_rectangle,
    draw_circle,
    draw_square,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    flood_fill,
)

pygame.init()

# Window settings
WIDTH, HEIGHT = 1300, 800
TOOLBAR_H = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint")
clock = pygame.time.Clock()

# Canvas
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill((255, 255, 255))

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
GREEN = (60, 180, 90)
BLUE = (70, 120, 220)
YELLOW = (240, 220, 70)
PURPLE = (170, 90, 220)
GRAY = (220, 220, 220)
LIGHT_GRAY = (245, 245, 245)

font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 28)

# Tools and state
tool = "pencil"
color = BLACK
drawing = False
start_pos = None
last_pos = None
brush_size = 2

# Text tool state
text_mode = False
text_position = None
typed_text = ""

# Colors
colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE]
color_rects = [pygame.Rect(20 + i * 45, 20, 30, 30) for i in range(len(colors))]

# Tool buttons
tool_buttons = {
    "pencil": pygame.Rect(320, 10, 110, 30),
    "line": pygame.Rect(440, 10, 110, 30),
    "rect": pygame.Rect(560, 10, 110, 30),
    "circle": pygame.Rect(680, 10, 110, 30),
    "eraser": pygame.Rect(800, 10, 110, 30),
    "fill": pygame.Rect(920, 10, 110, 30),
    "text": pygame.Rect(1040, 10, 110, 30),
    "clear": pygame.Rect(1160, 10, 110, 30),

    "square": pygame.Rect(320, 50, 110, 30),
    "rtriangle": pygame.Rect(440, 50, 110, 30),
    "etriangle": pygame.Rect(560, 50, 110, 30),
    "rhombus": pygame.Rect(680, 50, 110, 30),
}

# Brush size buttons
size_buttons = {
    "small": pygame.Rect(920, 50, 70, 30),
    "medium": pygame.Rect(1000, 50, 70, 30),
    "large": pygame.Rect(1080, 50, 70, 30),
}


def get_size_name():
    if brush_size == 2:
        return "small"
    if brush_size == 5:
        return "medium"
    return "large"


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_H))

    # Color buttons
    for i, rect in enumerate(color_rects):
        pygame.draw.rect(screen, colors[i], rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Tool buttons
    for name, rect in tool_buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(name.capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 8, rect.y + 7))

    # Size buttons
    current_size = get_size_name()
    for name, rect in size_buttons.items():
        fill = LIGHT_GRAY if name == current_size else WHITE
        pygame.draw.rect(screen, fill, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        label = font.render(name.capitalize(), True, BLACK)
        screen.blit(label, (rect.x + 7, rect.y + 7))

    info1 = font.render(f"Tool: {tool}", True, BLACK)
    info2 = font.render(f"Brush size: {brush_size}", True, BLACK)
    info3 = font.render("Keys: 1-small  2-medium  3-large  Ctrl+S-save", True, BLACK)

    screen.blit(info1, (20, 60))
    screen.blit(info2, (150, 60))
    screen.blit(info3, (20, 80))


def apply_shape(surface, tool_name, color_value, p1, p2, width):
    if tool_name == "line":
        draw_line(surface, color_value, p1, p2, width)
    elif tool_name == "rect":
        draw_rectangle(surface, color_value, p1, p2, width)
    elif tool_name == "circle":
        draw_circle(surface, color_value, p1, p2, width)
    elif tool_name == "square":
        draw_square(surface, color_value, p1, p2, width)
    elif tool_name == "rtriangle":
        draw_right_triangle(surface, color_value, p1, p2, width)
    elif tool_name == "etriangle":
        draw_equilateral_triangle(surface, color_value, p1, p2, width)
    elif tool_name == "rhombus":
        draw_rhombus(surface, color_value, p1, p2, width)


while True:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_H))
    draw_toolbar()

    # Live preview for shapes and line
    if drawing and tool in ["line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus"] and start_pos:
        mx, my = pygame.mouse.get_pos()
        end_pos = (mx, my - TOOLBAR_H)

        preview = canvas.copy()
        apply_shape(preview, tool, color, start_pos, end_pos, brush_size)
        screen.blit(preview, (0, TOOLBAR_H))

    # Live preview for text
    if text_mode and text_position:
        preview = canvas.copy()
        text_surface = text_font.render(typed_text, True, color)
        preview.blit(text_surface, text_position)
        screen.blit(preview, (0, TOOLBAR_H))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            # Brush size shortcuts
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            # Save canvas: Ctrl+S
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = "canvas_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
                pygame.image.save(canvas, filename)
                print(f"Saved: {filename}")

            # Text mode typing
            if text_mode:
                if event.key == pygame.K_RETURN:
                    if typed_text:
                        text_surface = text_font.render(typed_text, True, color)
                        canvas.blit(text_surface, text_position)
                    text_mode = False
                    text_position = None
                    typed_text = ""
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_position = None
                    typed_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                else:
                    if event.unicode.isprintable():
                        typed_text += event.unicode

        # Mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Click on toolbar
            if my <= TOOLBAR_H:
                for i, rect in enumerate(color_rects):
                    if rect.collidepoint(mx, my):
                        color = colors[i]

                for name, rect in tool_buttons.items():
                    if rect.collidepoint(mx, my):
                        if name == "clear":
                            canvas.fill(WHITE)
                        else:
                            tool = name
                            text_mode = False
                            typed_text = ""

                for name, rect in size_buttons.items():
                    if rect.collidepoint(mx, my):
                        if name == "small":
                            brush_size = 2
                        elif name == "medium":
                            brush_size = 5
                        elif name == "large":
                            brush_size = 10

            # Click on canvas
            else:
                canvas_pos = (mx, my - TOOLBAR_H)

                # Fill tool
                if tool == "fill":
                    flood_fill(canvas, canvas_pos, color)

                # Text tool
                elif tool == "text":
                    text_mode = True
                    text_position = canvas_pos
                    typed_text = ""

                else:
                    drawing = True
                    start_pos = canvas_pos
                    last_pos = canvas_pos

                    if tool == "pencil":
                        pygame.draw.circle(canvas, color, canvas_pos, max(1, brush_size // 2))
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_pos, max(1, brush_size // 2))

        # Mouse motion
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my > TOOLBAR_H:
                current_pos = (mx, my - TOOLBAR_H)

                if tool == "pencil":
                    draw_line(canvas, color, last_pos, current_pos, brush_size)
                    last_pos = current_pos

                elif tool == "eraser":
                    draw_line(canvas, WHITE, last_pos, current_pos, brush_size)
                    last_pos = current_pos

        # Mouse up
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            mx, my = event.pos
            if my > TOOLBAR_H:
                end_pos = (mx, my - TOOLBAR_H)

                if tool in ["line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus"]:
                    apply_shape(canvas, tool, color, start_pos, end_pos, brush_size)

            drawing = False
            start_pos = None
            last_pos = None

    pygame.display.flip()
    clock.tick(60)