"""
Pull full-resolution images from a public Instagram post.

Instagram's post HTML contains several signed CDN URLs per image. Most are
capped (`_s640x640` + `dst-jpg`), but the *cover* image of the currently
selected carousel slide is also present uncapped -- and that one serves the
image at native resolution.

So: walk the carousel with ?img_index=N, grab the uncapped signed URL each
page exposes, and dedupe. Public pages, documented query parameter, no auth.
"""
import hashlib
import io
import os
import re
import sys
import urllib.request
from PIL import Image

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
SIGNED = re.compile(
    r'https://[a-z0-9\-.]*(?:fbcdn\.net|cdninstagram\.com)/v/t51\.[0-9\-]+/[^"\\ ]*oe=[0-9A-Fa-f]+'
)


def get(url, binary=False):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.instagram.com/",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def uncapped_urls(html):
    """Signed URLs with no size cap and no jpg transcode -> native resolution."""
    html = html.replace("\\u0026", "&").replace("\\/", "/")
    out = []
    for m in SIGNED.finditer(html):
        u = m.group(0).replace("&amp;", "&")
        if "t51.2885-19" in u:          # profile avatars
            continue
        if re.search(r"_s\d+x\d+", u):  # size-capped variant
            continue
        if "dst-jpg" in u:              # transcoded variant
            continue
        out.append(u)
    return out


def main(shortcode, slides=12):
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "full_" + shortcode)
    os.makedirs(outdir, exist_ok=True)

    seen_url, seen_hash, saved = set(), set(), 0
    print(f"{'slide':<7}{'result':<44}{'size':>12}")
    print("-" * 64)

    for idx in range(1, slides + 1):
        url = f"https://www.instagram.com/p/{shortcode}/?img_index={idx}"
        try:
            html = get(url)
        except Exception as e:
            print(f"{idx:<7}page error: {e}")
            continue

        found = [u for u in uncapped_urls(html) if u not in seen_url]
        if not found:
            print(f"{idx:<7}(no new uncapped url)")
            continue

        for u in found:
            seen_url.add(u)
            try:
                blob = get(u, binary=True)
            except Exception as e:
                print(f"{idx:<7}download error: {e}")
                continue

            h = hashlib.md5(blob).hexdigest()
            if h in seen_hash:
                print(f"{idx:<7}duplicate image, skipped")
                continue
            seen_hash.add(h)

            im = Image.open(io.BytesIO(blob)).convert("RGB")
            saved += 1
            path = os.path.join(outdir, f"f{saved:02d}.jpg")
            im.save(path, "JPEG", quality=95, subsampling=0)
            print(f"{idx:<7}f{saved:02d}.jpg{'':<34}{im.width}x{im.height:>6}")

    print("-" * 64)
    print(f"{saved} unique full-res images -> {outdir}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 12)
