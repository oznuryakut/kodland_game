from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Cloud Runner"

TILE_W = 64
TILE_H = 24
GROUND_Y = HEIGHT - TILE_H

def actor_rect(actor):
    return Rect(actor.left, actor.top, actor.width, actor.height)


def play_sound(name):
    if sound_on:
        getattr(sounds, name).play()


class AnimatedActor:
    ...

class AnimatedActor:
    # Karakter animasyonlarını yönetir

    animation_speed = 0.12

    def __init__(self, idle_frames, walk_frames, pos):
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.actor = Actor(idle_frames[0], pos)
        self.frame_index = 0
        self.frame_timer = 0.0
        self.facing_right = True
        self.is_moving = False

    def _frame_list(self):
        frames = self.walk_frames if self.is_moving else self.idle_frames
        if self.facing_right:
            return frames
        return [name + "_l" for name in frames]

    def animate(self, dt):
        frames = self._frame_list()
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0.0
            self.frame_index += 1
        self.frame_index %= len(frames)
        self.actor.image = frames[self.frame_index]

    def draw(self):
        self.actor.draw()



class Hero(AnimatedActor):
    SPEED = 200
    GRAVITY = 900
    JUMP_SPEED = -480

    def __init__(self, pos):
        idle_frames = ["hero_idle_0", "hero_idle_1"]
        walk_frames = ["hero_walk_0", "hero_walk_1", "hero_walk_2", "hero_walk_3"]
        super().__init__(idle_frames, walk_frames, pos)
        self.velocity_y = 0.0
        self.on_ground = False
        self.alive = True

    def _read_input(self):
        dx = 0
        moving = False
        if keyboard.left or keyboard.a:
            dx -= self.SPEED
            self.facing_right = False
            moving = True
        if keyboard.right or keyboard.d:
            dx += self.SPEED
            self.facing_right = True
            moving = True
        self.is_moving = moving
        return dx

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.JUMP_SPEED
            self.on_ground = False
            play_sound("jump")

    def check_platform(self, platforms, previous_bottom):
        self.on_ground = False
        if self.velocity_y < 0:
            return
        hero_rect = actor_rect(self.actor)
        for platform in platforms:
            overlaps_x = (hero_rect.right > platform.rect.left
                          and hero_rect.left < platform.rect.right)
            if not overlaps_x:
                continue
            crossed_top = (previous_bottom <= platform.rect.top + 1
                           and hero_rect.bottom >= platform.rect.top)
            if crossed_top:
                self.actor.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
                break

    def update(self, dt, platforms):
        if not self.alive:
            return
        dx = self._read_input()
        self.actor.x += dx * dt
        self.actor.x = max(20, min(WIDTH - 20, self.actor.x))

        previous_bottom = self.actor.bottom
        self.velocity_y += self.GRAVITY * dt
        self.actor.y += self.velocity_y * dt
        self.check_platform(platforms, previous_bottom)

        if self.actor.y > HEIGHT + 60:
            self.alive = False

        self.animate(dt)

class Enemy(AnimatedActor):
    # Düşman belirlenen alanda gidip gelir

    def __init__(self, idle_frames, walk_frames, pos, min_x, max_x, speed):
        super().__init__(idle_frames, walk_frames, pos)
        self.min_x = min_x
        self.max_x = max_x
        self.speed = speed
        self.is_moving = True

    def update(self, dt):
        self.actor.x += self.speed * dt
        if self.actor.x <= self.min_x:
            self.actor.x = self.min_x
            self.speed = abs(self.speed)
            self.facing_right = True
        elif self.actor.x >= self.max_x:
            self.actor.x = self.max_x
            self.speed = -abs(self.speed)
            self.facing_right = False
        self.animate(dt)

    def hits(self, hero):
        return actor_rect(self.actor).colliderect(actor_rect(hero.actor))


class Platform:
    def __init__(self, x, y, tiles):
        self.x = x
        self.y = y
        self.tiles = tiles
        self.rect = Rect(x, y, tiles * TILE_W, TILE_H)

    def draw(self):
        for i in range(self.tiles):
            screen.blit("platform", (self.x + i * TILE_W, self.y))


class Coin:
    FRAMES = ["coin_0", "coin_1", "coin_2", "coin_3"]

    def __init__(self, pos):
        self.actor = Actor(self.FRAMES[0], pos)
        self.frame_index = 0
        self.timer = 0.0
        self.collected = False

    def update(self, dt):
        if self.collected:
            return
        self.timer += dt
        if self.timer >= 0.1:
            self.timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.FRAMES)
            self.actor.image = self.FRAMES[self.frame_index]

    def draw(self):
        if not self.collected:
            self.actor.draw()

    def collected_by(self, hero):
        if self.collected:
            return False
        if actor_rect(self.actor).colliderect(actor_rect(hero.actor)):
            self.collected = True
            return True
        return False


class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = Rect(x, y, width, height)
        self.callback = callback

    def draw(self):
        screen.draw.filled_rect(self.rect, (45, 55, 90))
        screen.draw.rect(self.rect, (230, 230, 240))
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=30,
            color="white",
            owidth=0.5,
            ocolor="black",
        )

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False



game_state = "menu"
sound_on = True
score = 0
hero = None
platforms = []
coins = []
enemies = []


def build_level():
    global hero, platforms, coins, enemies, score
    score = 0
    platforms = [
        Platform(0, GROUND_Y, 13),
        Platform(120, 480, 3),
        Platform(320, 390, 3),
        Platform(520, 300, 3),
    ]
    hero = Hero((60, GROUND_Y - 40))
    coins = [
        Coin((190, 450)),
        Coin((400, 360)),
        Coin((600, 270)),
    ]
    enemies = [
        Enemy(
            ["enemy1_idle_0", "enemy1_idle_1"],
            ["enemy1_walk_0", "enemy1_walk_1", "enemy1_walk_2", "enemy1_walk_3"],
            (250, GROUND_Y - 20),
            min_x=90,
            max_x=650,
            speed=70,
        ),
        Enemy(
            ["enemy2_idle_0", "enemy2_idle_1"],
            ["enemy2_walk_0", "enemy2_walk_1", "enemy2_walk_2", "enemy2_walk_3"],
            (420, 340),
            min_x=340,
            max_x=600,
            speed=110,
        ),
    ]


def flag_rect():
    platform = platforms[-1]
    return Rect(platform.x + platform.tiles * TILE_W - 40, platform.y - 64, 40, 64)


def start_game():
    global game_state
    build_level()
    game_state = "playing"
    if sound_on:
        music.play("theme")


def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        music.play("theme")
    else:
        music.stop()


def go_to_menu():
    global game_state
    game_state = "menu"


def exit_game():
    quit()


menu_buttons = [
    Button("Oyuna Basla", WIDTH / 2 - 110, 260, 220, 56, start_game),
    Button("Ses Ac/Kapat", WIDTH / 2 - 110, 330, 220, 56, toggle_sound),
    Button("Cikis", WIDTH / 2 - 110, 400, 220, 56, exit_game),
]

end_buttons = [
    Button("Tekrar Oyna", WIDTH / 2 - 110, 340, 220, 56, start_game),
    Button("Ana Menu", WIDTH / 2 - 110, 410, 220, 56, go_to_menu),
]


def update(dt):
    global game_state, score
    if game_state != "playing":
        return

    hero.update(dt, platforms)
    for enemy in enemies:
        enemy.update(dt)
    for coin in coins:
        coin.update(dt)
        if coin.collected_by(hero):
            score += 1
            play_sound("coin")

    for enemy in enemies:
        if enemy.hits(hero):
            play_sound("hit")
            game_state = "lose"
            music.stop()
            return

    if not hero.alive:
        play_sound("hit")
        game_state = "lose"
        music.stop()
        return

    if actor_rect(hero.actor).colliderect(flag_rect()):
        play_sound("win")
        game_state = "win"
        music.stop()


def draw():
    screen.blit("background", (0, 0))

    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_gameplay()
    elif game_state == "win":
        draw_end_screen("Kazandin!", (60, 170, 90))
    elif game_state == "lose":
        draw_end_screen("Kaybettin!", (170, 60, 60))


def draw_menu():
    screen.draw.text(
        TITLE, center=(WIDTH / 2, 150), fontsize=64, color="white", owidth=1, ocolor="black"
    )
    for button in menu_buttons:
        button.draw()
    status = "Ses: Acik" if sound_on else "Ses: Kapali"
    screen.draw.text(status, center=(WIDTH / 2, 470), fontsize=24, color="white")


def draw_gameplay():
    for platform in platforms:
        platform.draw()
    screen.blit("flag", (flag_rect().x, flag_rect().y))
    for coin in coins:
        coin.draw()
    for enemy in enemies:
        enemy.draw()
    hero.draw()
    screen.draw.text(f"Coins: {score}/{len(coins)}", (16, 12), fontsize=28, color="white")


def draw_end_screen(title, color):
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0))
    screen.draw.text(title, center=(WIDTH / 2, 220), fontsize=56, color=color)
    coin_text = f"Toplanan coin: {score}/{len(coins)}"
    screen.draw.text(coin_text, center=(WIDTH / 2, 280), fontsize=28, color="white")
    for button in end_buttons:
        button.draw()


def on_mouse_down(pos):
    if game_state == "menu":
        for button in menu_buttons:
            if button.handle_click(pos):
                play_sound("click")
                break
    elif game_state in ("win", "lose"):
        for button in end_buttons:
            if button.handle_click(pos):
                play_sound("click")
                break


def on_key_down(key):
    if game_state == "playing" and key in (keys.SPACE, keys.UP, keys.W):
        hero.jump()
