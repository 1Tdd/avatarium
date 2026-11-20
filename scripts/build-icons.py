"""Draws the app icons used when the site is added to a phone's home screen (public/icon-*.png).
The face of the logo sits inside the central safe zone, so launchers may crop the corners to any shape."""
import pathlib
from PIL import Image, ImageChops, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[1]
BG, LIME, INK = '#0c0e0f', '#d8f36a', '#10130a'
S = 1024  # drawn once at high resolution, then scaled down


def icon():
    img = Image.new('RGB', (S, S), BG)
    # The face's 42-unit disc (centre 27,37 on the logo's 64-unit grid) fills 62% of the icon.
    K = S * 0.62 / 42
    def P(x, y): return (S / 2 + (x - 27) * K, S / 2 + (y - 37) * K)
    ImageDraw.Draw(img).ellipse([*P(6, 16), *P(48, 58)], fill=LIME)
    face = Image.new('L', (S, S), 0)
    f = ImageDraw.Draw(face)
    f.line([P(5, 25), P(49, 40)], fill=255, width=round(2.6 * K))
    eye = Image.new('L', (S, S), 0)
    ImageDraw.Draw(eye).ellipse([*P(35.5 - 6.8, 34.5 - 6.2), *P(35.5 + 6.8, 34.5 + 6.2)], fill=255)
    face = ImageChops.lighter(face, eye.rotate(-18, center=P(35.5, 34.5)))
    f = ImageDraw.Draw(face)
    f.ellipse([*P(18.5 - 3.3, 34 - 3.3), *P(18.5 + 3.3, 34 + 3.3)], fill=255)
    smile = [P((1 - t) ** 2 * 17.5 + 2 * (1 - t) * t * 25.5 + t * t * 35, (1 - t) ** 2 * 45.5 + 2 * (1 - t) * t * 52.5 + t * t * 46.5) for t in [i / 400 for i in range(401)]]
    # A round pen moved along the curve gives a smooth stroke with round ends.
    for x, y in smile:
        f.ellipse([x - 1.5 * K, y - 1.5 * K, x + 1.5 * K, y + 1.5 * K], fill=255)
    disc = Image.new('L', (S, S), 0)
    ImageDraw.Draw(disc).ellipse([*P(6, 16), *P(48, 58)], fill=255)
    img.paste(INK, mask=ImageChops.multiply(face, disc))
    return img


big = icon()
for size, name in [(512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')]:
    out = ROOT / 'public' / name
    big.resize((size, size), Image.LANCZOS).save(out, optimize=True)
    print(out.name, out.stat().st_size, 'bytes')
