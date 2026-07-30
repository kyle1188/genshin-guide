# -*- coding: utf-8 -*-
"""Overlay promo titles + domain on 5 longtail AI base images -> 4:5 Twitter/X & Xiaohongshu PNGs."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "E:/workbuddy/2026-07-29-09-05-15/genshin-guide/assets/promo_longtail"
FONT = "C:/Windows/Fonts/msyh.ttc"
def font(sz): return ImageFont.truetype(FONT, sz)

GOLD = (255, 215, 120)
WHITE = (245, 247, 252)
DARK = (8, 11, 18)

DOMAIN = "genshin-guide-one-five.vercel.app"

# (src, out, title, sub, tag)
jobs = [
    ("Genshin_Impact_fan_art_style_i_2026-07-29T10-36-38.png",
     "promo_chars_en.png",
     "Best F2P Characters",
     "Which 4-star units to build first",
     "Free starter guide ->"),
    ("Genshin_Impact_fan_art_style___2026-07-29T10-37-09.png",
     "promo_artifact_en.png",
     "Artifact Farming Guide",
     "Which sets to farm first + resin route",
     "Start smart ->"),
    ("Genshin_Impact_fan_art_style_p_2026-07-29T10-37-39.png",
     "promo_furina_en.png",
     "Furina Build 2026",
     "Best weapons, Golden Troupe & teams",
     "Build guide ->"),
    ("Genshin_Impact_fan_art_style___2026-07-29T10-38-09.png",
     "promo_chars_zh.png",
     "原神新手必练角色",
     "平民 / 零氪性价比清单",
     "开荒不踩坑 ->"),
    ("Genshin_Impact_fan_art_style_p_2026-07-29T10-38-38.png",
     "promo_cover.png",
     "Teyvat Starter Guides",
     "Free Genshin guides for new Travelers",
     "Explore all guides ->"),
]

for src, out, title, sub, tag in jobs:
    p = os.path.join(BASE, src)
    img = Image.open(p).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    # bottom gradient panel for text readability
    panel_h = int(h * 0.38)
    for y in range(h - panel_h, h):
        t = (y - (h - panel_h)) / panel_h
        a = int(220 * (0.35 + 0.65 * t))
        draw.line([(0, y), (w, y)], fill=(6, 9, 16, a))

    # opaque corner patch to cover the AI watermark
    cw, ch = 300, 110
    draw.rounded_rectangle([w - cw - 10, h - ch - 5, w - 5, h - 5], radius=20, fill=(6, 9, 16, 255))

    cx = w // 2
    draw.text((cx, h - panel_h + 90), title, font=font(58), fill=GOLD, anchor="mm")
    draw.text((cx, h - panel_h + 165), sub, font=font(34), fill=WHITE, anchor="mm")
    draw.text((cx, h - panel_h + 220), tag, font=font(30), fill=(200, 210, 230), anchor="mm")

    pw, ph = 720, 70
    px0, py0 = cx - pw // 2, h - 95
    draw.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=35, fill=(20, 30, 50, 230), outline=GOLD, width=3)
    draw.text((cx, py0 + ph // 2), DOMAIN, font=font(34), fill=GOLD, anchor="mm")

    outp = os.path.join(BASE, out)
    img.save(outp, "PNG")
    print("SAVED", outp, img.size)
