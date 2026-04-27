import os
import random
import time
import pygame

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)
RED = (220, 60, 60)
BLUE = (70, 120, 220)
GREEN = (60, 180, 90)
YELLOW = (240, 220, 70)
PURPLE = (170, 90, 220)
ORANGE = (255, 165, 0)
CYAN = (0, 200, 220)

ROAD_LEFT = 50
ROAD_RIGHT = 350
LANE_CENTERS = [100, 200, 300]
FINISH_DISTANCE = 15000


class Player:
    def __init__(self, game, car_color):
        self.game = game

        color_map = {
            "blue": "blue_player.png",
            "red": "red_player.png",
            "green": "green_player.png",
            "yellow": "yellow_player.png",
        }

        filename = color_map.get(car_color, "blue_player.png")
        player_path = os.path.join(game.assets_dir, filename)

        print("Loading player image from:", player_path)

        self.image = pygame.image.load(player_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect(center=(200, 520))

        self.base_speed = 6
        self.current_speed = 6
        self.shield = False
        self.repair = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.current_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.current_speed

        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.shield:
            shield_rect = self.rect.inflate(14, 14)
            pygame.draw.rect(surface, PURPLE, shield_rect, 3)


class TrafficCar:
    def __init__(self, game, lane, speed):
        self.game = game
        self.image = pygame.image.load(game.enemy_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect(center=(LANE_CENTERS[lane], -100))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Obstacle:
    def __init__(self, lane, obstacle_type, speed):
        self.type = obstacle_type
        self.speed = speed

        if obstacle_type == "barrier":
            self.rect = pygame.Rect(0, -50, 70, 25)
            self.color = BLACK
        elif obstacle_type == "oil":
            self.rect = pygame.Rect(0, -40, 60, 30)
            self.color = (40, 40, 40)
        elif obstacle_type == "slow":
            self.rect = pygame.Rect(0, -40, 70, 20)
            self.color = ORANGE
        else:
            self.rect = pygame.Rect(0, -35, 55, 25)
            self.color = GRAY

        self.rect.centerx = LANE_CENTERS[lane]

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        if self.type == "oil":
            pygame.draw.ellipse(surface, self.color, self.rect)
        elif self.type == "pothole":
            pygame.draw.ellipse(surface, BLACK, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)


class RoadEvent:
    def __init__(self, lane, event_type, speed):
        self.type = event_type
        self.speed = speed

        if event_type == "moving_barrier":
            self.rect = pygame.Rect(0, -40, 75, 20)
            self.rect.centerx = LANE_CENTERS[lane]
            self.direction = random.choice([-2, 2])
            self.color = BLACK
        elif event_type == "speed_bump":
            self.rect = pygame.Rect(0, -30, 70, 12)
            self.rect.centerx = LANE_CENTERS[lane]
            self.color = ORANGE
        else:
            self.rect = pygame.Rect(0, -60, 70, 40)
            self.rect.centerx = LANE_CENTERS[lane]
            self.color = CYAN

    def update(self):
        self.rect.y += self.speed
        if self.type == "moving_barrier":
            self.rect.x += self.direction
            if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
                self.direction *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Coin:
    def __init__(self, game, lane, speed):
        self.game = game
        self.original_image = pygame.image.load(game.coin_img_path).convert_alpha()

        self.weight = random.choice([1, 2, 3])
        if self.weight == 1:
            size = 22
            self.value = 1
        elif self.weight == 2:
            size = 28
            self.value = 2
        else:
            size = 34
            self.value = 3

        self.image = pygame.transform.scale(self.original_image, (size, size))
        self.rect = self.image.get_rect(center=(LANE_CENTERS[lane], -60))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class PowerUp:
    def __init__(self, lane, kind, speed):
        self.kind = kind
        self.speed = speed
        self.timeout = time.time() + 5
        self.rect = pygame.Rect(0, -40, 35, 35)
        self.rect.centerx = LANE_CENTERS[lane]

        if kind == "nitro":
            self.color = CYAN
        elif kind == "shield":
            self.color = PURPLE
        else:
            self.color = GREEN

    def update(self):
        self.rect.y += self.speed

    def expired(self):
        return time.time() > self.timeout

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)


class RacerGame:
    def __init__(self, settings, username):
        self.width = 400
        self.height = 600
        self.settings = settings
        self.username = username.strip() if username.strip() else "Player"

        base_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(base_dir, "assets")

        self.road_img_path = os.path.join(self.assets_dir, "AnimatedStreet.png")
        self.enemy_img_path = os.path.join(self.assets_dir, "Enemy.png")
        self.coin_img_path = os.path.join(self.assets_dir, "Coin.png")
        self.bg_sound_path = os.path.join(self.assets_dir, "background.wav")
        self.crash_sound_path = os.path.join(self.assets_dir, "crash.wav")


        self.background = pygame.image.load(self.road_img_path).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.scroll_y1 = 0
        self.scroll_y2 = -self.height

        self.player = Player(self, settings["car_color"])

        self.coins = []
        self.traffic = []
        self.obstacles = []
        self.events = []
        self.powerups = []

        self.game_over = False
        self.finished = False
        self.crash_played = False

        self.coins_collected = 0
        self.score = 0
        self.distance = 0
        self.max_distance = FINISH_DISTANCE

        self.active_power = None
        self.power_end_time = 0

        self.spawn_timer_coin = 0
        self.spawn_timer_traffic = 0
        self.spawn_timer_obstacle = 0
        self.spawn_timer_event = 0
        self.spawn_timer_power = 0

        self.difficulty_multiplier = 1.0
        self.base_scroll_speed = 5
        self.enemy_speed = 5

        if settings["difficulty"] == "easy":
            self.base_scroll_speed = 4
            self.enemy_speed = 4
        elif settings["difficulty"] == "hard":
            self.base_scroll_speed = 6
            self.enemy_speed = 6

        self.sound_enabled = settings["sound"]
        self.crash_sound = None

        if pygame.mixer.get_init():
            try:
                self.crash_sound = pygame.mixer.Sound(self.crash_sound_path)
                self.crash_sound.set_volume(0.8)

                if self.sound_enabled:
                    pygame.mixer.music.load(self.bg_sound_path)
                    pygame.mixer.music.set_volume(0.35)
                    pygame.mixer.music.play(-1)
            except Exception:
                self.crash_sound = None

    def stop_audio(self):
        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

    def play_crash(self):
        if self.sound_enabled and self.crash_sound and not self.crash_played:
            self.stop_audio()
            self.crash_sound.play()
            self.crash_played = True

    def road_speed(self):
        if self.active_power == "nitro":
            return self.base_scroll_speed + 4
        return self.base_scroll_speed

    def update(self):
        if self.game_over or self.finished:
            return

        self.player.current_speed = self.player.base_speed
        self.player.update()

        self.distance += self.road_speed()
        self.score = self.coins_collected * 10 + self.distance // 10
        self.difficulty_multiplier = 1 + self.distance / 3000

        if self.settings["difficulty"] == "easy":
            base_enemy = 4
        elif self.settings["difficulty"] == "hard":
            base_enemy = 6
        else:
            base_enemy = 5

        self.enemy_speed = int(base_enemy * self.difficulty_multiplier)

        if self.distance >= self.max_distance:
            self.finished = True
            self.stop_audio()
            return

        if self.active_power == "nitro" and time.time() > self.power_end_time:
            self.active_power = None
        if self.active_power == "shield" and not self.player.shield:
            self.active_power = None

        speed = self.road_speed()
        self.scroll_y1 += speed
        self.scroll_y2 += speed

        if self.scroll_y1 >= self.height:
            self.scroll_y1 = -self.height
        if self.scroll_y2 >= self.height:
            self.scroll_y2 = -self.height

        self.spawn_objects()

        for lst in [self.coins, self.traffic, self.obstacles, self.events, self.powerups]:
            for obj in lst:
                obj.update()

        self.coins = [x for x in self.coins if x.rect.top < self.height]
        self.traffic = [x for x in self.traffic if x.rect.top < self.height]
        self.obstacles = [x for x in self.obstacles if x.rect.top < self.height]
        self.events = [x for x in self.events if x.rect.top < self.height]
        self.powerups = [x for x in self.powerups if x.rect.top < self.height and not x.expired()]

        self.handle_collisions()

    def lane_safe_for_spawn(self, lane):
        player_lane = min(range(3), key=lambda i: abs(LANE_CENTERS[i] - self.player.rect.centerx))
        return lane != player_lane

    def spawn_objects(self):
        now = pygame.time.get_ticks()

        coin_interval = max(500, int(1200 / self.difficulty_multiplier))
        traffic_interval = max(700, int(1800 / self.difficulty_multiplier))
        obstacle_interval = max(800, int(2200 / self.difficulty_multiplier))
        event_interval = 3500
        power_interval = 5000

        if now - self.spawn_timer_coin > coin_interval:
            lane = random.randint(0, 2)
            if self.lane_safe_for_spawn(lane):
                self.coins.append(Coin(self, lane, self.road_speed()))
            self.spawn_timer_coin = now

        if now - self.spawn_timer_traffic > traffic_interval:
            lane = random.randint(0, 2)
            if self.lane_safe_for_spawn(lane):
                self.traffic.append(TrafficCar(self, lane, self.enemy_speed))
            self.spawn_timer_traffic = now

        if now - self.spawn_timer_obstacle > obstacle_interval:
            lane = random.randint(0, 2)
            if self.lane_safe_for_spawn(lane):
                kind = random.choice(["barrier", "oil", "slow", "pothole"])
                self.obstacles.append(Obstacle(lane, kind, self.road_speed()))
            self.spawn_timer_obstacle = now

        if now - self.spawn_timer_event > event_interval:
            lane = random.randint(0, 2)
            if self.lane_safe_for_spawn(lane):
                kind = random.choice(["moving_barrier", "speed_bump", "nitro_strip"])
                self.events.append(RoadEvent(lane, kind, self.road_speed()))
            self.spawn_timer_event = now

        if now - self.spawn_timer_power > power_interval:
            lane = random.randint(0, 2)
            if self.lane_safe_for_spawn(lane):
                kind = random.choice(["nitro", "shield", "repair"])
                self.powerups.append(PowerUp(lane, kind, self.road_speed()))
            self.spawn_timer_power = now

    def use_collision_protection(self):
        if self.player.shield:
            self.player.shield = False
            self.active_power = None
            return True
        if self.player.repair > 0:
            self.player.repair -= 1
            return True
        return False

    def handle_collisions(self):
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins_collected += coin.value
                self.score += coin.value * 10
                self.coins.remove(coin)

        for car in self.traffic[:]:
            if self.player.rect.colliderect(car.rect):
                if self.use_collision_protection():
                    self.traffic.remove(car)
                else:
                    self.game_over = True
                    self.play_crash()
                break

        for obs in self.obstacles[:]:
            if self.player.rect.colliderect(obs.rect):
                if obs.type == "oil":
                    self.player.rect.x += random.choice([-40, 40])
                elif obs.type == "slow":
                    self.player.current_speed = 3
                else:
                    if self.use_collision_protection():
                        self.obstacles.remove(obs)
                    else:
                        self.game_over = True
                        self.play_crash()
                    break

        for ev in self.events[:]:
            if self.player.rect.colliderect(ev.rect):
                if ev.type == "nitro_strip":
                    self.active_power = "nitro"
                    self.power_end_time = time.time() + 4
                elif ev.type == "speed_bump":
                    self.player.current_speed = 3
                else:
                    if self.use_collision_protection():
                        self.events.remove(ev)
                    else:
                        self.game_over = True
                        self.play_crash()
                    break

        for p in self.powerups[:]:
            if self.player.rect.colliderect(p.rect):
                self.active_power = None
                self.player.shield = False

                if p.kind == "nitro":
                    self.active_power = "nitro"
                    self.power_end_time = time.time() + 4
                elif p.kind == "shield":
                    self.active_power = "shield"
                    self.player.shield = True
                else:
                    self.player.repair = 1

                self.powerups.remove(p)

    def draw_road(self, surface):
        surface.blit(self.background, (0, self.scroll_y1))
        surface.blit(self.background, (0, self.scroll_y2))

    def draw(self, surface, font, small_font):
        self.draw_road(surface)

        for obj in self.coins:
            obj.draw(surface)
        for obj in self.traffic:
            obj.draw(surface)
        for obj in self.obstacles:
            obj.draw(surface)
        for obj in self.events:
            obj.draw(surface)
        for obj in self.powerups:
            obj.draw(surface)

        self.player.draw(surface)

        remaining = max(0, self.max_distance - self.distance)

        surface.blit(font.render(f"Coins: {self.coins_collected}", True, BLACK), (10, 10))
        surface.blit(font.render(f"Score: {int(self.score)}", True, BLACK), (10, 35))
        surface.blit(font.render(f"Distance: {int(self.distance)}", True, BLACK), (10, 60))
        surface.blit(font.render(f"Left: {int(remaining)}", True, BLACK), (10, 85))

        if self.active_power == "nitro":
            left = max(0, int(self.power_end_time - time.time()))
            surface.blit(font.render(f"Power: Nitro {left}s", True, BLACK), (190, 10))
        elif self.player.shield:
            surface.blit(font.render("Power: Shield", True, BLACK), (190, 10))
        elif self.player.repair > 0:
            surface.blit(font.render("Power: Repair", True, BLACK), (190, 10))
        else:
            surface.blit(font.render("Power: None", True, BLACK), (190, 10))