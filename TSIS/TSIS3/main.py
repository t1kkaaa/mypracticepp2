import sys
import pygame

from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import Button, draw_center_text, draw_left_text, WHITE, BLACK, RED, BLUE
from racer import RacerGame

pygame.init()

try:
    pygame.mixer.init()
except Exception:
    pass

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)
big_font = pygame.font.SysFont("Arial", 34)

settings = load_settings()

state = "menu"
username = ""
game = None

menu_buttons = [
    Button((120, 200, 160, 45), "Play"),
    Button((120, 260, 160, 45), "Leaderboard"),
    Button((120, 320, 160, 45), "Settings"),
    Button((120, 380, 160, 45), "Quit"),
]

leaderboard_back = Button((120, 520, 160, 40), "Back")
settings_back = Button((120, 520, 160, 40), "Back")
gameover_retry = Button((120, 380, 160, 40), "Retry")
gameover_menu = Button((120, 440, 160, 40), "Main Menu")

sound_button = Button((110, 180, 180, 40), "Toggle Sound")
color_button = Button((110, 250, 180, 40), "Car Color")
difficulty_button = Button((110, 320, 180, 40), "Difficulty")


def cycle_car_color():
    colors = ["blue", "red", "green", "yellow"]
    idx = colors.index(settings["car_color"])
    settings["car_color"] = colors[(idx + 1) % len(colors)]


def cycle_difficulty():
    levels = ["easy", "normal", "hard"]
    idx = levels.index(settings["difficulty"])
    settings["difficulty"] = levels[(idx + 1) % len(levels)]


def start_game():
    global game, state
    game = RacerGame(settings, username)
    state = "game"


while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if game:
                game.stop_audio()
            pygame.quit()
            sys.exit()

        if state == "menu":
            if menu_buttons[0].is_clicked(event):
                state = "name_input"
                username = ""
            elif menu_buttons[1].is_clicked(event):
                state = "leaderboard"
            elif menu_buttons[2].is_clicked(event):
                state = "settings"
            elif menu_buttons[3].is_clicked(event):
                if game:
                    game.stop_audio()
                pygame.quit()
                sys.exit()

        elif state == "name_input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"
                elif event.unicode.isprintable():
                    username += event.unicode

        elif state == "settings":
            if sound_button.is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            elif color_button.is_clicked(event):
                cycle_car_color()
                save_settings(settings)
            elif difficulty_button.is_clicked(event):
                cycle_difficulty()
                save_settings(settings)
            elif settings_back.is_clicked(event):
                state = "menu"

        elif state == "leaderboard":
            if leaderboard_back.is_clicked(event):
                state = "menu"

        elif state == "game":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game:
                    game.stop_audio()
                state = "menu"

        elif state == "game_over":
            if gameover_retry.is_clicked(event):
                start_game()
            elif gameover_menu.is_clicked(event):
                state = "menu"

        elif state == "finished":
            if gameover_retry.is_clicked(event):
                start_game()
            elif gameover_menu.is_clicked(event):
                state = "menu"

    if state == "game":
        game.update()
        if game.game_over:
            add_score(game.username, int(game.score), int(game.distance), game.coins_collected)
            state = "game_over"
        elif game.finished:
            add_score(game.username, int(game.score + 500), int(game.distance), game.coins_collected)
            state = "finished"

    screen.fill((230, 230, 230))

    if state == "menu":
        draw_center_text(screen, "RACER MENU", big_font, BLACK, 100)
        for b in menu_buttons:
            b.draw(screen, font, mouse_pos)

    elif state == "name_input":
        draw_center_text(screen, "ENTER USERNAME", big_font, BLACK, 150)
        pygame.draw.rect(screen, WHITE, (70, 250, 260, 50))
        pygame.draw.rect(screen, BLACK, (70, 250, 260, 50), 2)
        draw_left_text(screen, username, font, BLACK, 80, 262)
        draw_center_text(screen, "Press Enter to start", small_font, BLACK, 340)
        draw_center_text(screen, "Press Esc to go back", small_font, BLACK, 370)

    elif state == "settings":
        draw_center_text(screen, "SETTINGS", big_font, BLACK, 90)
        sound_button.draw(screen, font, mouse_pos)
        color_button.draw(screen, font, mouse_pos)
        difficulty_button.draw(screen, font, mouse_pos)
        settings_back.draw(screen, font, mouse_pos)

        draw_center_text(screen, f"Sound: {'On' if settings['sound'] else 'Off'}", small_font, BLACK, 235)
        draw_center_text(screen, f"Car color: {settings['car_color']}", small_font, BLACK, 305)
        draw_center_text(screen, f"Difficulty: {settings['difficulty']}", small_font, BLACK, 375)

    elif state == "leaderboard":
        draw_center_text(screen, "TOP 10", big_font, BLACK, 70)
        entries = load_leaderboard()

        y = 120
        if not entries:
            draw_center_text(screen, "No scores yet", font, BLACK, 180)
        else:
            for i, entry in enumerate(entries, start=1):
                text = f"{i}. {entry['name']}  S:{entry['score']}  D:{entry['distance']}"
                draw_left_text(screen, text, small_font, BLACK, 25, y)
                y += 35

        leaderboard_back.draw(screen, font, mouse_pos)

    elif state == "game":
        game.draw(screen, font, small_font)

    elif state == "game_over":
        draw_center_text(screen, "GAME OVER", big_font, RED, 150)
        draw_center_text(screen, f"Score: {int(game.score)}", font, BLACK, 230)
        draw_center_text(screen, f"Distance: {int(game.distance)}", font, BLACK, 265)
        draw_center_text(screen, f"Coins: {game.coins_collected}", font, BLACK, 300)
        gameover_retry.draw(screen, font, mouse_pos)
        gameover_menu.draw(screen, font, mouse_pos)

    elif state == "finished":
        draw_center_text(screen, "FINISH!", big_font, BLUE, 150)
        draw_center_text(screen, f"Score: {int(game.score + 500)}", font, BLACK, 230)
        draw_center_text(screen, f"Distance: {int(game.distance)}", font, BLACK, 265)
        draw_center_text(screen, f"Coins: {game.coins_collected}", font, BLACK, 300)
        gameover_retry.draw(screen, font, mouse_pos)
        gameover_menu.draw(screen, font, mouse_pos)

    pygame.display.flip()
    clock.tick(60)