#!/usr/bin/env python3
"""Builds the site's logo, tab icons and link-preview image in img/ from the
master logo, design/firegrid-logo.webp. Rerun it after changing the logo:

    python3 deploy/make-icons.py        (needs Pillow: pip install pillow)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design" / "firegrid-logo.webp"
OUT = ROOT / "img"
BG = (13, 17, 16)                 # the site's --bg, #0d1110


def master():
    im = Image.open(SRC).convert("RGBA")
    # the WebP's alpha sits at 252-253 inside the badge; make that solid so
    # the icons aren't faintly see-through
    im.putalpha(im.getchannel("A").point(lambda a: 255 if a >= 240 else a))
    return im


def square(im, size):
    return im.resize((size, size), Image.LANCZOS)


def small_png(im):
    """256 colours: a third of the size, and no visible difference at icon size."""
    return im.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)


def on_background(im, size, pad):
    """The badge centred on the site colour: for places with no transparency."""
    canvas = Image.new("RGBA", (size, size), BG + (255,))
    inner = square(im, size - 2 * pad)
    canvas.alpha_composite(inner, (pad, pad))
    return canvas.convert("RGB")


def preview(im, w=1200, h=630):
    """Wide link preview (Discord, Reddit, Steam): badge on a dark glow."""
    canvas = Image.new("RGB", (w, h), BG)
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse((w / 2 - 330, h / 2 - 330, w / 2 + 330, h / 2 + 330), fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    canvas.paste(Image.new("RGB", (w, h), (60, 90, 60)), (0, 0), glow)
    badge = square(im, 590)
    canvas.paste(badge, ((w - 590) // 2, (h - 590) // 2), badge)
    return canvas


def main():
    OUT.mkdir(exist_ok=True)
    im = master()

    # on the page: the home-page badge (1x and 2x) and the top-bar mark
    for size in (320, 640):
        square(im, size).save(OUT / f"firegrid-logo-{size}.webp", quality=82, method=6)
    square(im, 96).save(OUT / "firegrid-mark-96.webp", quality=88, method=6)

    # tab icons: .ico for every browser, PNGs for Android/Chrome, and iOS's
    # home-screen icon (iOS fills transparency with black, so give it the site colour)
    im.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    small_png(square(im, 192)).save(OUT / "icon-192.png", optimize=True)
    small_png(on_background(im, 180, 6)).save(OUT / "apple-touch-icon.png", optimize=True)

    preview(im).save(OUT / "og-image.jpg", quality=85, optimize=True, progressive=True)

    for p in sorted(OUT.iterdir()):
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
