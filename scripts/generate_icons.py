"""Generate PNG icons for PWA (Chrome refuses SVG icons reliably).

Run once:
    uv run --with Pillow python -m scripts.generate_icons
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

BG = (30, 27, 75, 255)        # #1e1b4b
GOLD = (251, 191, 36, 255)    # #fbbf24
GOLD_DARK = (180, 83, 9, 255) # #b45309


def _scale(s: int, val: int) -> int:
    return round(val * s / 192)


def draw_trophy(size: int, out: Path) -> None:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    sc = lambda v: _scale(size, v)

    # rounded square background
    d.rounded_rectangle((0, 0, size, size), radius=sc(36), fill=BG)

    # left handle (ring opening to the left)
    d.arc((sc(38), sc(58), sc(72), sc(104)),
          start=90, end=270, fill=GOLD, width=sc(7))
    # right handle
    d.arc((sc(120), sc(58), sc(154), sc(104)),
          start=-90, end=90, fill=GOLD, width=sc(7))

    # cup body
    d.rounded_rectangle((sc(62), sc(50), sc(130), sc(114)),
                        radius=sc(8), fill=GOLD)
    # subtle inner shade to give depth
    d.rectangle((sc(62), sc(50), sc(130), sc(60)), fill=(253, 224, 71, 255))

    # stem
    d.rectangle((sc(88), sc(114), sc(104), sc(134)), fill=GOLD)

    # base (two-tier)
    d.rounded_rectangle((sc(68), sc(134), sc(124), sc(146)),
                        radius=sc(3), fill=GOLD)
    d.rounded_rectangle((sc(60), sc(146), sc(132), sc(156)),
                        radius=sc(2), fill=GOLD_DARK)

    img.save(out, "PNG", optimize=True)
    print(f"Wrote {out} ({size}x{size})")


def main() -> int:
    out_dir = Path(__file__).parent.parent / "public"
    out_dir.mkdir(parents=True, exist_ok=True)
    draw_trophy(192, out_dir / "icon-192.png")
    draw_trophy(512, out_dir / "icon-512.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
