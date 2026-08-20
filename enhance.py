"""
Clean up and upscale the 640px Instagram stills for use on the site.

What this can honestly do:
  - remove JPEG blocking/ringing artifacts from IG's recompression
  - upscale with Lanczos (much better than the browser's bilinear stretch)
  - restore local micro-contrast with a tuned unsharp mask
  - crop to each slot's exact aspect ratio, biased so faces don't get cut

What it CANNOT do: invent detail that Instagram threw away. Upscaling is
capped at 2x so we sharpen real information instead of amplifying mush.
"""
import os
from PIL import Image, ImageFilter, ImageEnhance

SRC = os.path.join(os.path.dirname(__file__), "ig")
OUT = r"c:\Users\Acer\Documents\demo\assets\img"
MAX_UPSCALE = 2.0

# slot -> (source, target_w, target_h, vertical_crop_bias)
# bias: 0.0 = keep top of frame, 0.5 = centre, 1.0 = keep bottom
JOBS = [
    ("hero.jpg",     "p03.jpg", 1920, 1080, 0.45),
    ("about-1.jpg",  "p09.jpg",  900, 1200, 0.42),
    ("about-2.jpg",  "p08.jpg", 1200,  900, 0.45),
    ("work-01.jpg",  "p05.jpg",  900, 1500, 0.40),
    ("work-02.jpg",  "p04.jpg", 1200,  900, 0.40),
    ("work-03.jpg",  "p06.jpg", 1200,  900, 0.45),
    ("work-04.jpg",  "p01.jpg", 1600,  600, 0.45),
    ("work-05.jpg",  "p07.jpg", 1200,  900, 0.55),
    ("work-06.jpg",  "p02.jpg",  900, 1500, 0.35),
    ("og-cover.jpg", "p04.jpg", 1200,  630, 0.40),
]


def cover_crop(im, tw, th, bias=0.5):
    """Crop to the target aspect ratio, keeping as much of the frame as possible."""
    sw, sh = im.size
    target_ar, src_ar = tw / th, sw / sh
    if src_ar > target_ar:                      # too wide -> trim sides (centred)
        new_w = round(sh * target_ar)
        left = (sw - new_w) // 2
        box = (left, 0, left + new_w, sh)
    else:                                       # too tall -> trim top/bottom (biased)
        new_h = round(sw / target_ar)
        top = round((sh - new_h) * bias)
        box = (0, top, sw, top + new_h)
    return im.crop(box)


def enhance(im, tw, th):
    cw, ch = im.size
    # cap the upscale so we sharpen real detail rather than amplifying artifacts
    scale = min(MAX_UPSCALE, max(tw / cw, th / ch))
    scale = max(scale, 1.0)
    ow, oh = round(cw * scale), round(ch * scale)

    # 1. knock back JPEG blocking BEFORE enlarging, so it isn't magnified too
    im = im.filter(ImageFilter.GaussianBlur(0.45))
    im = im.filter(ImageFilter.MedianFilter(3))

    # 2. Lanczos upscale
    im = im.resize((ow, oh), Image.LANCZOS)

    # 3. two-stage sharpening: broad structure, then fine edges
    im = im.filter(ImageFilter.UnsharpMask(radius=2.4, percent=85,  threshold=4))
    im = im.filter(ImageFilter.UnsharpMask(radius=0.9, percent=125, threshold=2))

    # 4. gentle grade — IG's recompression flattens contrast and colour
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.09)
    im = ImageEnhance.Brightness(im).enhance(1.02)
    return im


print(f"{'output':<14}{'source':<10}{'from':>12}{'to':>14}{'size':>10}")
print("-" * 62)
total = 0
for dest, src, tw, th, bias in JOBS:
    sp = os.path.join(SRC, src)
    im = Image.open(sp).convert("RGB")
    before = f"{im.width}x{im.height}"
    im = cover_crop(im, tw, th, bias)
    im = enhance(im, tw, th)
    dp = os.path.join(OUT, dest)
    im.save(dp, "JPEG", quality=90, subsampling=0, optimize=True, progressive=True)
    kb = os.path.getsize(dp) / 1024
    total += kb
    print(f"{dest:<14}{src:<10}{before:>12}{im.width}x{im.height:>8}{kb:>8.0f} KB")

print("-" * 62)
print(f"{'total':<36}{total:>24.0f} KB")
