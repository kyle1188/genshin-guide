# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1080, 1350
IMG = Image.new("RGB", (W, H), (10, 14, 22))
draw = ImageDraw.Draw(IMG)

# ---- background gradient (deep blue -> black) ----
top = (18, 28, 48)
bot = (8, 11, 18)
for y in range(H):
    t = y / H
    r = int(top[0] + (bot[0]-top[0])*t)
    g = int(top[1] + (bot[1]-top[1])*t)
    b = int(top[2] + (bot[2]-top[2])*t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ---- decorative element orbs (gold/blue glow) ----
def orb(cx, cy, rad, color):
    for i in range(rad, 0, -2):
        a = int(40 * (i/rad))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=color)

orb(120, 140, 70, (60, 90, 160))
orb(980, 200, 55, (150, 120, 50))
orb(940, 1180, 80, (40, 70, 140))
orb(150, 1120, 60, (140, 110, 45))

FONT = "C:/Windows/Fonts/msyh.ttc"
def font(sz): return ImageFont.truetype(FONT, sz)

GOLD = (212, 175, 90)
WHITE = (235, 238, 245)
SUB = (150, 165, 190)

# ---- kicker ----
draw.text((W//2, 150), "FREE BILINGUAL GUIDE", font=font(34), fill=GOLD, anchor="mm")

# ---- main title (zh) ----
draw.text((W//2, 250), "原神新手攻略", font=font(96), fill=GOLD, anchor="mm")

# ---- subtitle (en) ----
draw.text((W//2, 350), "Genshin Impact Beginner Guide", font=font(40), fill=WHITE, anchor="mm")

# ---- 5 tools ----
tools = [
    ("1", "抽卡模拟器  Gacha Simulator"),
    ("2", "元素反应演示  Element Demo"),
    ("3", "原石规划器  Primogem Planner"),
    ("4", "配队共鸣  Team Resonance"),
    ("5", "开荒打卡  Onboarding Checklist"),
]
y = 500
for num, label in tools:
    # number circle
    draw.ellipse([120, y-42, 204, y+42], fill=(212, 175, 90))
    draw.text((162, y), num, font=font(48), fill=(10, 14, 22), anchor="mm")
    draw.text((250, y), label, font=font(42), fill=WHITE, anchor="lm")
    y += 120

# ---- domain pill ----
pill_h = 96
py = H - 150
draw.rounded_rectangle([110, py, W-110, py+pill_h], radius=48, fill=(20, 30, 50), outline=GOLD, width=3)
draw.text((W//2, py+pill_h//2), "genshin-guide-one-five.vercel.app", font=font(38), fill=GOLD, anchor="mm")

# ---- footer hint ----
draw.text((W//2, H-60), "5 interactive tools · CN / EN auto", font=font(30), fill=SUB, anchor="mm")

OUT = "E:/workbuddy/2026-07-29-09-05-15/genshin-guide/assets/twitter-card.png"
IMG.save(OUT, "PNG")
print("SAVED", OUT, IMG.size)
