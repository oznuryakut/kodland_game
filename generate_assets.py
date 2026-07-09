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
    # Oyuncu karakterini çizer
    img = new_canvas(w, h)
    d = ImageDraw.Draw(img)
    cx = w // 2
    top = 4 + bob

    # Kafa
    d.ellipse([cx - 8, top, cx + 8, top + 16], fill=(255, 214, 170, 255),
              outline=(60, 40, 30, 255), width=2)
    d.ellipse([cx - 3, top + 5, cx, top + 8], fill=(40, 30, 25, 255))
    d.ellipse([cx + 1, top + 5, cx + 4, top + 8], fill=(40, 30, 25, 255))

    # Gövde
    body_top = top + 16
    body_bottom = body_top + 20
    body_box = [cx - 9, body_top, cx + 9, body_bottom]
    outline_color = (30, 30, 30, 255)
    d.rounded_rectangle(body_box, radius=4, fill=body_color, outline=outline_color, width=2)

    # Kollar
    d.line([cx - 9, body_top + 4, cx - 9 - leg_offset*-0 + -arm_offset],
           fill=body_color, width=5)
    d.line([cx + 9, body_top + 4, cx + 9 + arm_offset],
           fill=body_color, width=5)

    # Bacaklar
    leg_top = body_bottom
    d.line([cx - 4, leg_top, cx - 4 - leg_offset, leg_top + 14], fill=(50,60,90,255), width=6)
    d.line([cx + 4, leg_top, cx + 4 + leg_offset, leg_top + 14], fill=(50,60,90,255), width=6)
    return img

print("Resimler olusturuldu")
