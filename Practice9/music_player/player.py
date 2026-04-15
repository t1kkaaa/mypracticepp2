import os
import pygame


class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()

        self.music_folder = music_folder
        self.playlist = self.load_tracks()
        self.current_index = 0
        self.is_playing = False
        self.current_track_length = 0

    def load_tracks(self):
        tracks = []

        if os.path.exists(self.music_folder):
            for file_name in os.listdir(self.music_folder):
                lower_name = file_name.lower()
                if lower_name.endswith(".mp3") or lower_name.endswith(".wav"):
                    full_path = os.path.join(self.music_folder, file_name)
                    tracks.append(full_path)

        tracks.sort()
        return tracks

    def play(self):
        if not self.playlist:
            return

        track = self.playlist[self.current_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.is_playing = True

        try:
            sound = pygame.mixer.Sound(track)
            self.current_track_length = sound.get_length()
        except pygame.error:
            self.current_track_length = 0

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_index])

    def get_position(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0.0
        return pos_ms / 1000

    def update_auto_next(self):
        if self.is_playing and self.playlist and not pygame.mixer.music.get_busy():
            self.next_track()