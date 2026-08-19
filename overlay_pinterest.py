# -*- coding: utf-8 -*-
"""Overlay Pinterest 2:3 infographic (title + 3-line build + domain) on 3 vertical AI base images."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "E:/workbuddy/2026-07-29-09-05-15/genshin-guide/assets/promo_pinterest"
FONT = "C:/Windows/Fonts/msyh.ttc"
def font(sz): return ImageFont.truetype(FONT, sz)

GOLD = (255, 215, 120)
WHITE = (245, 247, 252)
SOFT = (200, 210, 230)
DARK = (8, 11, 18)
DOMAIN = "genshin-guide-one-five.vercel.app"

# (src, out, title, sub, weapon, artifact, mainstats)
jobs = [
    ("Genshin_Impact_fan_art_style_v_2026-08-04T23-20-53.png", "pin_albedo.png",
     "Albedo Build Guide", "Genshin Impact \u00b7 2026 Best Builds",
     "Weapon: Cinnabar Spindle R5", "Artifact: 4pc Husk of Opulent Dreams",
     "Main Stats: DEF% \u00b7 Geo DMG \u00b7 CRIT"),
    ("Genshin_Impact_fan_art_style_v_2026-08-04T23-21-23.png", "pin_xiao.png",
     "Xiao Build Guide", "Genshin Impact \u00b7 2026 Best Builds",
     "Weapon: Primordial Jade Winged-Spear", "Artifact: 4pc Vermillion Hereafter",
     "Main Stats: ATK% \u00b7 Anemo DMG \u00b7 CRIT"),
    ("Genshin_Impact_fan_art_style_v_2026-08-04T23-22-53.png", "pin_yaemiko.png",
     "Yae Miko Build Guide", "Genshin Impact \u00b7 2026 Best Builds",
     "Weapon: Kagura's Verity", "Artifact: 4pc Golden Troupe",
     "Main Stats: ATK% \u00b7 Electro DMG \u00b7 CRIT"),
]

for src, out, title, sub, wpn, art, mst in jobs:
    p = os.path.join(BASE, src)
    img = Image.open(p).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    # bottom gradient panel (taller, darker base -> title readable)
    panel_h = int(h * 0.58)
    for y in range(h - panel_h, h):
        t = (y - (h - panel_h)) / panel_h
        a = int(240 * (0.60 + 0.40 * t))
        draw.line([(0, y), (w, y)], fill=(4, 6, 12, a))

    # opaque corner patch to cover AI watermark (bottom-right)
    cw, ch = 320, 120
    draw.rounded_rectangle([w - cw - 10, h - ch - 5, w - 5, h - 5], radius=20, fill=(4, 6, 12, 255))

    cx = w // 2
    ptop = h - panel_h

    # title
    draw.text((cx, ptop + 90), title, font=font(68), fill=GOLD, anchor="mm")
    # subtitle
    draw.text((cx, ptop + 160), sub, font=font(34), fill=WHITE, anchor="mm")

    # build info card (each line centered as a whole string)
    card_top = ptop + 210
    line_gap = 54
    lines = [wpn, art, mst]
    card_h = line_gap * len(lines) + 36
    cw2 = int(w * 0.88)
    cx0, cy0 = cx - cw2 // 2, card_top
    draw.rounded_rectangle([cx0, cy0, cx0 + cw2, cy0 + card_h], radius=18,
                           fill=(10, 16, 28, 210), outline=GOLD, width=2)
    for i, ln in enumerate(lines):
        ly = cy0 + 30 + i * line_gap + line_gap // 2
        # color the label portion (before ':') gold, rest white, all centered as one block
        if ":" in ln:
            lab, val = ln.split(":", 1)
            lab_text = lab + ":"
            val_text = val  # leading space already in val? ensure single space
            if not val_text.startswith(" "):
                val_text = " " + val_text
            lw = draw.textlength(lab_text, font=font(32))
            vw = draw.textlength(val_text, font=font(32))
            total = lw + vw
            x0 = cx - total / 2
            draw.text((x0, ly), lab_text, font=font(32), fill=GOLD, anchor="lm")
            draw.text((x0 + lw, ly), val_text, font=font(32), fill=WHITE, anchor="lm")
        else:
            draw.text((cx, ly), ln, font=font(32), fill=WHITE, anchor="mm")

    # domain pill
    pw, ph = 760, 70
    px0, py0 = cx - pw // 2, h - 100
    draw.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=35,
                           fill=(20, 30, 50, 235), outline=GOLD, width=3)
    draw.text((cx, py0 + ph // 2), DOMAIN, font=font(34), fill=GOLD, anchor="mm")

    outp = os.path.join(BASE, out)
    img.save(outp, "PNG")
    print("SAVED", outp, img.size)