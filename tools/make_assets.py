#!/usr/bin/env python3
"""Generate Zeront brand assets: favicon set + OG image.
Radar mark: dark rounded square, green concentric rings, center dot,
one red blip. Drawn at 1024 and downscaled for crisp small sizes."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BG = (12, 18, 25)
GREEN = (47, 191, 113)
GREEN_DIM = (31, 122, 74)
RED = (230, 57, 70)
TXT = (233, 239, 245)
MUT = (157, 178, 198)

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# rounded square background
d.rounded_rectangle([0, 0, S - 1, S - 1], radius=200, fill=BG + (255,))
cx = cy = S // 2
# sweep wedge hint (composited layer, subtle)
wedge = Image.new("RGBA", (S, S), (0, 0, 0, 0))
wd = ImageDraw.Draw(wedge)
wd.pieslice([cx - 400, cy - 400, cx + 400, cy + 400], start=-38, end=0, fill=(47, 191, 113, 60))
img = Image.alpha_composite(img, wedge)
d = ImageDraw.Draw(img)
for r, w, col in [(400, 26, GREEN_DIM), (285, 26, GREEN_DIM), (170, 26, GREEN)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col + (255,), width=w)
# center dot
d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=GREEN + (255,))
# red blip on outer ring, upper right
import math
bx, by = cx + int(400 * math.cos(math.radians(-52))), cy + int(400 * math.sin(math.radians(-52)))
d.ellipse([bx - 62, by - 62, bx + 62, by + 62], fill=RED + (255,))
d.ellipse([bx - 26, by - 26, bx + 26, by + 26], fill=(255, 255, 255, 255))

img.save(ROOT / "icon-512.png")
img.resize((192, 192), Image.LANCZOS).save(ROOT / "icon-192.png")
img.resize((180, 180), Image.LANCZOS).save(ROOT / "apple-touch-icon.png")
img.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
<rect width="1024" height="1024" rx="200" fill="#0c1219"/>
<circle cx="512" cy="512" r="400" fill="none" stroke="#1f7a4a" stroke-width="26"/>
<circle cx="512" cy="512" r="285" fill="none" stroke="#1f7a4a" stroke-width="26"/>
<circle cx="512" cy="512" r="170" fill="none" stroke="#2fbf71" stroke-width="26"/>
<circle cx="512" cy="512" r="52" fill="#2fbf71"/>
<circle cx="757" cy="197" r="62" fill="#e63946"/>
<circle cx="757" cy="197" r="26" fill="#ffffff"/>
</svg>
"""
(ROOT / "favicon.svg").write_text(svg, encoding="utf-8")

# OG image 1200x630
W, H = 1200, 630
og = Image.new("RGB", (W, H), BG)
od = ImageDraw.Draw(og, "RGBA")
# radar rings on the right
rcx, rcy = 950, 315
for r, w, col in [(250, 5, GREEN_DIM), (175, 5, GREEN_DIM), (100, 5, GREEN)]:
    od.ellipse([rcx - r, rcy - r, rcx + r, rcy + r], outline=col, width=w)
od.pieslice([rcx - 250, rcy - 250, rcx + 250, rcy + 250], start=-38, end=0, fill=(47, 191, 113, 40))
od.ellipse([rcx - 16, rcy - 16, rcx + 16, rcy + 16], fill=GREEN)
od.ellipse([rcx + 130, rcy - 190, rcx + 162, rcy - 158], fill=RED)
od.ellipse([rcx - 60, rcy + 70, rcx - 36, rcy + 94], fill=RED)
f_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 92)
f_mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 30)
od.text((70, 150), "ZERONT", font=f_big, fill=TXT)
od.text((72, 268), "Radar lỗ hổng bảo mật", font=f_mid, fill=GREEN)
od.text((72, 330), "Lỗi đang bị khai thác thật trên thế giới,", font=f_mid, fill=MUT)
od.text((72, 382), "đối chiếu dữ liệu quét tại Việt Nam.", font=f_mid, fill=MUT)
od.text((72, 500), "secuscan.dannyphan.me/radar", font=f_small, fill=MUT)
og.save(ROOT / "og-image.png")
print("assets written:", [p.name for p in [ROOT / 'favicon.svg', ROOT / 'favicon.ico', ROOT / 'apple-touch-icon.png', ROOT / 'icon-192.png', ROOT / 'icon-512.png', ROOT / 'og-image.png']])
