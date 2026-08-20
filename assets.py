"""
Build the production image assets:
  1. a .webp beside every .jpg  (typically ~45% smaller, same quality)
  2. a tiny base64 LQIP per image, emitted as a CSS file

The LQIP is a 20px-wide blurred JPEG inlined as a background-image. It paints
instantly, so every frame has its own colour and composition on screen before
the real photo arrives -- no grey boxes, no layout pop.
"""
import base64
import io
import os
from PIL import Image, ImageFilter

IMG = r"c:\Users\Acer\Documents\demo\assets\img"
CSS = r"c:\Users\Acer\Documents\demo\assets\css\lqip.css"

rows, saved_jpg, saved_webp = [], 0, 0

for name in sorted(os.listdir(IMG)):
    if not name.endswith(".jpg"):
        continue
    path = os.path.join(IMG, name)
    im = Image.open(path).convert("RGB")
    stem = name[:-4]

    # --- webp twin ---
    wp = os.path.join(IMG, stem + ".webp")
    im.save(wp, "WEBP", quality=82, method=6)
    j, w = os.path.getsize(path), os.path.getsize(wp)
    saved_jpg += j
    saved_webp += w

    # --- LQIP ---
    lq = im.copy()
    lq.thumbnail((20, 20), Image.LANCZOS)
    lq = lq.filter(ImageFilter.GaussianBlur(0.6))
    buf = io.BytesIO()
    lq.save(buf, "JPEG", quality=42)
    b64 = base64.b64encode(buf.getvalue()).decode()
    rows.append((stem, b64, j, w))

with open(CSS, "w", encoding="utf-8") as f:
    f.write("/* Low-quality image placeholders - generated, do not edit by hand. */\n")
    f.write("/* Each paints instantly under its real photo so nothing pops in. */\n\n")
    for stem, b64, _, _ in rows:
        f.write(f'.lq-{stem}{{background-image:url("data:image/jpeg;base64,{b64}")}}\n')

print(f"{'image':<16}{'jpg':>9}{'webp':>9}{'saved':>8}   lqip")
print("-" * 56)
for stem, b64, j, w in rows:
    print(f"{stem:<16}{j/1024:>8.0f}K{w/1024:>8.0f}K{(1-w/j)*100:>7.0f}%{len(b64):>7}b")
print("-" * 56)
print(f"{'TOTAL':<16}{saved_jpg/1024:>8.0f}K{saved_webp/1024:>8.0f}K"
      f"{(1-saved_webp/saved_jpg)*100:>7.0f}%")
print(f"\nwrote {CSS}")
