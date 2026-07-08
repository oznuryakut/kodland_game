"""Generates all placeholder sprite / background assets for the game.

Run once with: python3 generate_assets.py
All art here is produced procedurally with Pillow so the project has
no external image dependencies (fully original, no third-party art).
"""
from PIL import Image, ImageDraw
import math
import os

IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)


def save(img, name):
    img.save(os.path.join(IMG_DIR, name))


def new_canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def draw_humanoid(w, h, body_color, leg_offset, arm_offset, bob):
    """Draws a simple stick-style humanoid used for the hero."""
    img = new_canvas(w, h)
    d = ImageDraw.Draw(img)
    cx = w // 2
    top = 4 + bob

    # Head
    d.ellipse([cx - 8, top, cx + 8, top + 16], fill=(255, 214, 170, 255),
              outline=(60, 40, 30, 255), width=2)
    d.ellipse([cx - 3, top + 5, cx, top + 8], fill=(40, 30, 25, 255))
    d.ellipse([cx + 1, top + 5, cx + 4, top + 8], fill=(40, 30, 25, 255))

    # Body
    body_top = top + 16
    body_bottom = body_top + 20
    body_box = [cx - 9, body_top, cx + 9, body_bottom]
    outline_color = (30, 30, 30, 255)
    d.rounded_rectangle(body_box, radius=4, fill=body_color, outline=outline_color, width=2)

    # Arms (swing opposite to legs)
    d.line([cx - 9, body_top + 4, cx - 9 - arm_offset, body_top + 14],
           fill=body_color, width=5)
    d.line([cx + 9, body_top + 4, cx + 9 + arm_offset, body_top + 14],
           fill=body_color, width=5)

    # Legs
    leg_top = body_bottom
    d.line([cx - 4, leg_top, cx - 4 - leg_offset, leg_top + 14],
           fill=(50, 60, 90, 255), width=6)
    d.line([cx + 4, leg_top, cx + 4 + leg_offset, leg_top + 14],
           fill=(50, 60, 90, 255), width=6)
    return img


def make_hero_frames():
    w, h = 40, 64
    # Idle: gentle bob, no leg/arm swing.
    save(draw_humanoid(w, h, (70, 130, 220, 255), 0, 0, 0), "hero_idle_0.png")
    save(draw_humanoid(w, h, (70, 130, 220, 255), 0, 0, 2), "hero_idle_1.png")
    # Walk cycle: legs and arms swing across four frames.
    swings = [-6, 0, 6, 0]
    for i, s in enumerate(swings):
        save(draw_humanoid(w, h, (70, 130, 220, 255), s, -s, 0), f"hero_walk_{i}.png")
    # Jump pose.
    save(draw_humanoid(w, h, (70, 130, 220, 255), -5, 8, -3), "hero_jump.png")


def draw_slime(w, h, color, squash, wobble):
    img = new_canvas(w, h)
    d = ImageDraw.Draw(img)
    cx = w // 2
    body_h = h - 14 - squash
    top = h - 6 - body_h
    d.ellipse([cx - 16, top, cx + 16, top + body_h + 12], fill=color,
              outline=(20, 20, 20, 255), width=2)
    eye_y = top + body_h // 2
    d.ellipse([cx - 8 + wobble, eye_y, cx - 4 + wobble, eye_y + 5], fill=(20, 20, 20, 255))
    d.ellipse([cx + 4 + wobble, eye_y, cx + 8 + wobble, eye_y + 5], fill=(20, 20, 20, 255))
    return img


def make_enemy1_frames():
    # A ground "slime" enemy that squashes as it scoots along the floor.
    w, h = 40, 40
    save(draw_slime(w, h, (210, 70, 70, 255), 2, 0), "enemy1_idle_0.png")
    save(draw_slime(w, h, (210, 70, 70, 255), 6, 0), "enemy1_idle_1.png")
    squashes = [2, 6, 10, 6]
    wobbles = [-2, 0, 2, 0]
    for i, (s, wob) in enumerate(zip(squashes, wobbles)):
        save(draw_slime(w, h, (210, 70, 70, 255), s, wob), f"enemy1_walk_{i}.png")


def draw_bat(w, h, color, wing_angle_deg, bob):
    img = new_canvas(w, h)
    d = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2 + bob
    # Body
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 8], fill=color, outline=(20, 20, 20, 255), width=2)
    d.ellipse([cx - 6, cy - 12, cx - 1, cy - 6], fill=color)
    d.ellipse([cx + 1, cy - 12, cx + 6, cy - 6], fill=color)
    # Wings, rotated around shoulder points to fake a flap animation.
    ang = math.radians(wing_angle_deg)
    for side in (-1, 1):
        sx, sy = cx + side * 6, cy - 2
        tip_x = sx + side * 16 * math.cos(ang)
        tip_y = sy - 16 * math.sin(ang)
        mid_x = sx + side * 10 * math.cos(ang * 0.5)
        mid_y = sy - 6
        wing_points = [(sx, sy), (mid_x, mid_y), (tip_x, tip_y)]
        d.polygon(wing_points, fill=color, outline=(20, 20, 20, 255))
    d.ellipse([cx - 3, cy, cx - 1, cy + 2], fill=(255, 255, 0, 255))
    d.ellipse([cx + 1, cy, cx + 3, cy + 2], fill=(255, 255, 0, 255))
    return img


def make_enemy2_frames():
    # A flying "bat" enemy that flaps its wings.
    w, h = 44, 40
    color = (120, 70, 160, 255)
    save(draw_bat(w, h, color, 25, 0), "enemy2_idle_0.png")
    save(draw_bat(w, h, color, 35, -2), "enemy2_idle_1.png")
    angles = [10, 45, 80, 45]
    for i, a in enumerate(angles):
        save(draw_bat(w, h, color, a, 0), f"enemy2_walk_{i}.png")


def make_platform_tile():
    w, h = 64, 24
    img = new_canvas(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], fill=(101, 67, 33, 255), outline=(60, 40, 20, 255), width=2)
    d.rectangle([0, 0, w - 1, 6], fill=(76, 175, 80, 255))
    save(img, "platform.png")


def make_background():
    w, h = 800, 600
    img = new_canvas(w, h)
    d = ImageDraw.Draw(img)
    top_color = (135, 206, 235)
    bottom_color = (200, 235, 245)
    for y in range(h):
        t = y / h
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        d.line([(0, y), (w, y)], fill=(r, g, b, 255))
    for cx, cy, r in [(120, 90, 30), (150, 90, 24), (500, 60, 26), (530, 70, 20)]:
        d.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], fill=(255, 255, 255, 230))
    save(img, "background.png")


def make_coin_frames():
    for i, squash in enumerate([16, 10, 4, 10]):
        img = new_canvas(24, 24)
        d = ImageDraw.Draw(img)
        d.ellipse([12 - squash // 2, 2, 12 + squash // 2, 22], fill=(255, 215, 0, 255),
                  outline=(150, 110, 0, 255), width=2)
        save(img, f"coin_{i}.png")


def make_flag():
    img = new_canvas(40, 64)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 0, 8, 64], fill=(90, 90, 90, 255))
    d.polygon([(8, 4), (36, 12), (8, 20)], fill=(220, 40, 40, 255))
    save(img, "flag.png")


def make_mirrored_copies():
    """Creates left-facing ('_l' suffix) mirrors for direction-aware sprites."""
    names = []
    for i in range(2):
        names.append(f"hero_idle_{i}.png")
    for i in range(4):
        names.append(f"hero_walk_{i}.png")
    names.append("hero_jump.png")
    for i in range(2):
        names.append(f"enemy1_idle_{i}.png")
    for i in range(4):
        names.append(f"enemy1_walk_{i}.png")
    for i in range(2):
        names.append(f"enemy2_idle_{i}.png")
    for i in range(4):
        names.append(f"enemy2_walk_{i}.png")

    for name in names:
        path = os.path.join(IMG_DIR, name)
        img = Image.open(path)
        mirrored = img.transpose(Image.FLIP_LEFT_RIGHT)
        base, ext = os.path.splitext(name)
        mirrored.save(os.path.join(IMG_DIR, f"{base}_l{ext}"))


make_hero_frames()
make_enemy1_frames()
make_enemy2_frames()
make_platform_tile()
make_background()
make_coin_frames()
make_flag()
make_mirrored_copies()
print("Assets generated.")
