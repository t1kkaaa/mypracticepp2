import os
import pygame
from player import MusicPlayer

WIDTH = 800
HEIGHT = 500

BG_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (255, 105, 180)
SECONDARY_COLOR = (200, 200, 200)


def draw_text(screen, text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Arial", 34, bold=True)
    font_medium = pygame.font.SysFont("Arial", 26)
    font_small = pygame.font.SysFont("Arial", 22)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    music_folder = os.path.join(base_dir, "musics")

    player = MusicPlayer(music_folder)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    running = False

        player.update_auto_next()

        screen.fill(BG_COLOR)

        draw_text(screen, "Music Player", font_big, ACCENT_COLOR, 280, 30)

        draw_text(
            screen,
            f"Current track: {player.get_current_track_name()}",
            font_medium,
            TEXT_COLOR,
            60,
            120
        )

        position = player.get_position()
        length = player.current_track_length

        draw_text(screen, f"Position: {position:.1f} sec", font_small, TEXT_COLOR, 60, 180)
        draw_text(screen, f"Length: {length:.1f} sec", font_small, TEXT_COLOR, 60, 220)

        controls = [
            "P = Play",
            "S = Stop",
            "N = Next track",
            "B = Previous track",
            "Q = Quit"
        ]

        y = 300
        for line in controls:
            draw_text(screen, line, font_small, SECONDARY_COLOR, 60, y)
            y += 35

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()