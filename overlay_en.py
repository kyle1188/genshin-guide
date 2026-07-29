# -*- coding: utf-8 -*-
"""Overlay English promo text + cover watermark on 3 AI images -> Twitter 4:5 PNGs."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "E:/workbuddy/2026-07-29-09-05-15/genshin-guide/assets"
FONT = "C:/Windows/Fonts/msyh.ttc"
def font(sz): return ImageFont.truetype(FONT, sz)

GOLD = (255, 215, 120)
WHITE = (245, 247, 252)
DARK = (8, 11, 18)

# (src, out, title_en, sub_en, tagline)
jobs = [
    ("A_breathtaking_panoramic_view__2026-07-29T07-52-00.png",
     "promo_en_teyvat.png",
     "Genshin Impact Beginner Guide",
     "Free bilingual walkthrough for new Travelers",
     "Start your journey ->"),
    ("A_spectacular_Genshin_Impact_e_2026-07-29T07-52-32.png",
     "promo_en_element.png",
     "Element Reaction Demo",
     "See Pyro x Hydro x Cryo x Electro in action",
     "Interactive tool ->"),
    ("A_magical_Genshin_Impact_gacha_2026-07-29T07-53-02.png",
     "promo_en_gacha.png",
     "Gacha Simulator",
     "Test your luck with real pity rules",
     "Free to play ->"),
]

DOMAIN = "genshin-guide-one-five.vercel.app"

for src, out, title, sub, tag in jobs:
    p = os.path.join(BASE, src)
    img = Image.open(p).convert("RGB")
    # crop to 4:5 if needed (1024x1536 already 4:5)
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    # bottom gradient panel for text readability
    panel_h = int(h * 0.38)
    for y in range(h - panel_h, h):
        t = (y - (h - panel_h)) / panel_h
        # overlay dark, stronger near bottom (covers watermark zone)
        a = int(220 * (0.35 + 0.65 * t))
        draw.line([(0, y), (w, y)], fill=(6, 9, 16, a))

    # extra opaque corner patch to guarantee watermark coverage
    cw, ch = 280, 100
    draw.rounded_rectangle([w - cw - 10, h - ch - 5, w - 5, h - 5], radius=20, fill=(6, 9, 16, 255))

    # top thin gold rule is optional; keep clean

    cx = w // 2
    # title
    draw.text((cx, h - panel_h + 90), title, font=font(58), fill=GOLD, anchor="mm")
    # subtitle
    draw.text((cx, h - panel_h + 165), sub, font=font(34), fill=WHITE, anchor="mm")
    # tagline
    draw.text((cx, h - panel_h + 220), tag, font=font(30), fill=(200, 210, 230), anchor="mm")
    # domain pill
    pw, ph = 720, 70
    px0, py0 = cx - pw // 2, h - 95
    draw.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=35, fill=(20, 30, 50, 230), outline=GOLD, width=3)
    draw.text((cx, py0 + ph // 2), DOMAIN, font=font(34), fill=GOLD, anchor="mm")

    outp = os.path.join(BASE, out)
    img.save(outp, "PNG")
    print("SAVED", outp, img.size)
