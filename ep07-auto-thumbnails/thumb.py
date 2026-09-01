"""Poster-frame generator — bold title card over a real image.

Usage: python3 poster.py <bg_image> <out.png> "TITLE LINE" [WxH] [highlight_word]
The poster becomes the video's first ~0.8s (feed freeze-frame + grid thumbnail).
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
HIGHLIGHT = (255, 215, 0)


def make(bg_path, out, title, size=(1080, 1920), highlight=None, purpose=None):
    W, H = size
    img = Image.open(bg_path).convert("RGB")
    w, h = img.size
    s = max(W / w, H / h)
    img = img.resize((int(w * s + 0.5), int(h * s + 0.5)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    img = img.crop((x, y, x + W, y + H))

    d = ImageDraw.Draw(img)
    words = title.upper().split()
    fs = int(H * 0.062)
    font = ImageFont.truetype(FONT, fs)
    # wrap to lines fitting 92% width
    lines, cur = [], []
    for wd in words:
        test = " ".join(cur + [wd])
        if d.textlength(test, font=font) > W * 0.92 and cur:
            lines.append(cur); cur = [wd]
        else:
            cur.append(wd)
    lines.append(cur)

    # Text block vertically CENTERED (grid badges cover top/bottom zones);
    # soft dark band behind it keeps it readable over any image.
    block_h = int(len(lines) * fs * 1.18)
    ty = (H - block_h) // 2
    band = Image.new("L", (1, H), 0)
    pad = int(fs * 1.2)
    for i in range(H):
        dist = 0 if ty - pad <= i <= ty + block_h + pad else min(
            abs(i - (ty - pad)), abs(i - (ty + block_h + pad)))
        band.putpixel((0, i), max(0, 165 - int(dist * 1.1)))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(dark, img, band.resize((W, H)))
    d = ImageDraw.Draw(img)
    for line in lines:
        lw = d.textlength(" ".join(line), font=font)
        tx = (W - lw) // 2
        for wd in line:
            color = HIGHLIGHT if highlight and highlight.upper() in wd else (255, 255, 255)
            d.text((tx, ty), wd, font=font, fill=color,
                   stroke_width=max(4, fs // 14), stroke_fill=(0, 0, 0))
            tx += d.textlength(wd + " ", font=font)
        ty += int(fs * 1.18)
    if purpose:
        # Shrink the purpose line until it fits the frame — it used to be drawn
        # at a fixed size and silently ran off both edges (caught 2026-08-25 on
        # the Rakhi poster: "...ence of Raksha Bandhan — in 60 s...").
        pfs = int(fs * 0.48)
        pfont = ImageFont.truetype(FONT, pfs)
        while d.textlength(purpose, font=pfont) > W * 0.90 and pfs > 14:
            pfs -= 2
            pfont = ImageFont.truetype(FONT, pfs)
        pw = d.textlength(purpose, font=pfont)
        d.text(((W - pw) // 2, ty + int(fs * 0.25)), purpose,
               font=pfont, fill=(210, 210, 210),
               stroke_width=max(2, pfs // 14), stroke_fill=(0, 0, 0))
    img.save(out, quality=93)
    print("poster:", out)


def make_stinger(series, episode, out, size=(1080, 1920)):
    """0.4s series brand card: dark bg, series name, episode number."""
    W, H = size
    img = Image.new("RGB", (W, H), (13, 17, 23))
    d = ImageDraw.Draw(img)
    fs = int(H * 0.05)
    t = series.upper()
    font = ImageFont.truetype(FONT, fs)
    while d.textlength(t, font=font) > W * 0.92 and fs > 20:
        fs -= 4
        font = ImageFont.truetype(FONT, fs)
    sfont = ImageFont.truetype(FONT, int(fs * 0.55))
    tw = d.textlength(t, font=font)
    d.text(((W - tw) // 2, H // 2 - fs), t, font=font, fill=(255, 215, 0),
           stroke_width=3, stroke_fill=(0, 0, 0))
    e = f"EPISODE {episode}"
    ew = d.textlength(e, font=sfont)
    d.text(((W - ew) // 2, H // 2 + int(fs * 0.5)), e, font=sfont,
           fill=(139, 148, 158))
    img.save(out, quality=93)
    print("stinger:", out)


if __name__ == "__main__":
    if sys.argv[1] == "stinger":
        series, ep, out = sys.argv[2], sys.argv[3], sys.argv[4]
        size = tuple(int(v) for v in (sys.argv[5] if len(sys.argv) > 5 else "1080x1920").split("x"))
        make_stinger(series, ep, out, size)
        sys.exit(0)
    bg, out, title = sys.argv[1:4]
    size = tuple(int(v) for v in (sys.argv[4] if len(sys.argv) > 4 else "1080x1920").split("x"))
    hl = sys.argv[5] if len(sys.argv) > 5 else None
    purpose = sys.argv[6] if len(sys.argv) > 6 else None
    make(bg, out, title, size, hl, purpose)
