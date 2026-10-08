#!/usr/bin/env python3
"""contact_sheet.py: tile rendered PNGs into one labelled sheet, for the look loop.

    python3 contact_sheet.py INPUT... --out sheet.png [--cols N] [--cell 360 | 390x844]
        [--bg '#808080' | checker] [--label stem|name|index|none] [--filmstrip]
        [--gap 8] [--title TEXT] [--every N] [--upscale] [--same-scale] [--allow-empty]
    python3 contact_sheet.py --selftest

Run it with a Python that has Pillow, e.g. ~/.venvs/flagship/bin/python (the skill's README shows the
two-line setup).

INPUT is any mix of image files, folders (every .png inside, in natural order: frame_2 before
frame_10) and glob patterns (quote them; the script expands them, also in natural order). Explicit
files keep the order given. A file path that does not exist is an error (exit 2), never skipped: a
before/after sheet that silently loses "before" looks like it worked. A folder or glob that matches
nothing is also an error, unless --allow-empty (then it is skipped with a note).

--cell N or WxH is the largest box an image is scaled DOWN into, aspect kept; it is never scaled up
unless --upscale (nearest neighbour, so pixels stay visible). For phone screens give the screen's
shape, e.g. --cell 390x844, so a tall screen fills its cell instead of shrinking into a square.
--same-scale uses one factor for every image, so two phone sizes or a row of icon sizes keep their
true relative size. All cells take the size of the largest scaled image (widened for its label up to
the --cell width), so rows and columns line up.

--filmstrip puts every image in one row: use it for sequences (transitions, a solve, a launch
handover), where order and timing faults only show side by side. --every N keeps every Nth image.

--bg is the sheet colour (default mid grey, which favours neither light nor dark art). "checker"
draws a checkerboard behind each image's own rectangle, so transparency and an icon's padding show
against the grey margin. Judge a look on its real background too: this sheet compares variants; it
does not judge contrast. Labels use Pillow's built-in Latin font: name files in ASCII.

Exit codes: 0 written; 1 bad arguments, an unreadable image or missing Pillow; 2 a missing input, an
input that matched nothing, or no images left to tile.
"""

from __future__ import annotations

import argparse
import glob
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

PILLOW_HELP = (
    "contact_sheet.py needs Pillow (the PIL package), and this Python cannot import it.\n"
    "A setup that works on every system Python (Homebrew and Linux distribution Pythons refuse a plain\n"
    "'pip install' under PEP 668):\n"
    "    python3 -m venv ~/.venvs/flagship\n"
    "    ~/.venvs/flagship/bin/pip install pillow\n"
    "then run this script with ~/.venvs/flagship/bin/python -I contact_sheet.py ...\n"
    "('python3 -I' ignores the user site folder, so a 'pip install --user' Pillow is invisible to it.)"
)
EXAMPLES = """examples (use the Python that has Pillow, e.g. ~/.venvs/flagship/bin/python):
  # every render of one look, phone-shaped cells, 4 columns
  python3 contact_sheet.py build/looks/home/ --cols 4 --cell 390x844 --title "look 2" --out build/looks/home_2.png
  # the smallest and a standard phone, at their true relative size
  python3 contact_sheet.py small/home.png standard/home.png --same-scale --cell 430x932 --out build/looks/sizes.png
  # a transition as a filmstrip, every 2nd frame, numbered
  python3 contact_sheet.py 'frames/arrive_*.png' --filmstrip --every 2 --cell 240x520 --label index --out build/looks/arrive.png
  # icon sizes on a checkerboard, so transparency and padding show
  python3 contact_sheet.py icon_1024.png icon_180.png icon_120.png --same-scale --bg checker --label name --out build/looks/icons.png
"""
MAX_SIDE = 20000
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")
GLOB_CHARS = "*?["


def _pil():
    """Imports Pillow, or exits 1 with install instructions."""
    try:
        from PIL import Image, ImageColor, ImageDraw, ImageFont  # noqa: F401
    except ImportError:
        print(PILLOW_HELP, file=sys.stderr)
        raise SystemExit(1)
    return Image, ImageColor, ImageDraw, ImageFont


def natural_key(path: str) -> List[object]:
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", os.path.basename(path))]


def expand(inputs: Sequence[str]) -> Tuple[List[str], List[str], List[str]]:
    """(images in order, explicit paths that do not exist, folders or globs that matched nothing)."""
    out: List[str] = []
    missing: List[str] = []
    empty: List[str] = []
    for item in inputs:
        if os.path.isdir(item):
            found = sorted((os.path.join(item, n) for n in os.listdir(item) if n.lower().endswith(".png")),
                           key=natural_key)
        elif os.path.isfile(item):
            out.append(item)
            continue
        elif not any(ch in item for ch in GLOB_CHARS):
            missing.append(item)
            continue
        else:
            found = sorted((p for p in glob.glob(item) if os.path.isfile(p) and p.lower().endswith(IMAGE_SUFFIXES)),
                           key=natural_key)
        if not found:
            empty.append(item)
        out.extend(found)
    return out, missing, empty


def parse_cell(text: str) -> Tuple[int, int]:
    m = re.fullmatch(r"(\d+)(?:x(\d+))?", text.strip().lower())
    if not m:
        raise argparse.ArgumentTypeError(f"--cell wants N or WxH (e.g. 390x844), got {text!r}")
    w = int(m.group(1))
    h = int(m.group(2) or m.group(1))
    if w < 8 or h < 8:
        raise argparse.ArgumentTypeError("--cell must be at least 8 px")
    return w, h


def label_for(path: str, index: int, mode: str) -> str:
    if mode == "name":
        return os.path.basename(path)
    if mode == "index":
        return f"{index + 1}. {Path(path).stem}"
    return Path(path).stem


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="contact_sheet.py", description="Tile PNGs into a labelled contact sheet "
                                "or filmstrip, for the look loop.", epilog=EXAMPLES,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("inputs", nargs="*", help="image files, folders (their .png files) or quoted globs")
    p.add_argument("--out", "-o", help="output PNG path (its folder is created)")
    p.add_argument("--cols", type=int, help="columns (default: ceil(sqrt(n)); ignored with --filmstrip)")
    p.add_argument("--cell", type=parse_cell, default=(360, 360),
                   help="largest box per image: N or WxH, e.g. 390x844 for phone screens (default 360)")
    p.add_argument("--bg", default="#808080", help="sheet colour, or 'checker' behind each image (default #808080)")
    p.add_argument("--label", choices=("stem", "name", "index", "none"), default="stem",
                   help="text under each image (default: file name without extension)")
    p.add_argument("--filmstrip", action="store_true", help="one row, in order")
    p.add_argument("--gap", type=int, default=8, help="space between cells, px (default 8)")
    p.add_argument("--title", help="a heading line above the sheet")
    p.add_argument("--every", type=int, default=1, help="keep every Nth image (default 1)")
    p.add_argument("--upscale", action="store_true", help="allow scaling small images up (nearest)")
    p.add_argument("--same-scale", dest="same_scale", action="store_true",
                   help="scale every image by one factor, so relative sizes stay true")
    p.add_argument("--allow-empty", dest="allow_empty", action="store_true",
                   help="skip a folder or glob that matches nothing instead of failing (missing files still fail)")
    p.add_argument("--selftest", action="store_true", help="prove this script works, in a temp folder")
    return p


def _font(ImageFont, size: int):
    try:
        return ImageFont.load_default(size=size)  # Pillow >= 10.1: a scalable face
    except TypeError:
        return ImageFont.load_default()


def _fit(text: str, draw, font, width: int) -> str:
    if draw.textlength(text, font=font) <= width:
        return text
    while text and draw.textlength(text + "...", font=font) > width:
        text = text[:-1]
    return text + "..."


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.out:
        print("contact_sheet: --out is required", file=sys.stderr)
        return 1
    if not args.inputs:
        print("contact_sheet: give at least one image, folder or glob", file=sys.stderr)
        return 1
    if args.every < 1 or args.gap < 0 or (args.cols is not None and args.cols < 1):
        print("contact_sheet: --every and --cols must be >= 1, --gap >= 0", file=sys.stderr)
        return 1
    found, missing, empty = expand(args.inputs)
    if missing:
        print("contact_sheet: no such file (nothing written):\n  " + "\n  ".join(missing), file=sys.stderr)
        return 2
    if empty and not args.allow_empty:
        print("contact_sheet: matched nothing (nothing written; --allow-empty skips these):\n  "
              + "\n  ".join(empty), file=sys.stderr)
        return 2
    for item in empty:
        print(f"contact_sheet: skipped, matched nothing: {item}", file=sys.stderr)
    paths = found[:: args.every]
    if not paths:
        print(f"contact_sheet: no images to tile from {list(args.inputs)}", file=sys.stderr)
        return 2
    out_real = os.path.realpath(args.out)
    if any(os.path.realpath(p) == out_real for p in paths):
        print(f"contact_sheet: --out {args.out} is also an input; refusing to overwrite it", file=sys.stderr)
        return 1
    Image, ImageColor, ImageDraw, ImageFont = _pil()
    checker = args.bg.strip().lower() == "checker"
    try:
        bg = (128, 128, 128) if checker else ImageColor.getrgb(args.bg)[:3]
    except ValueError:
        print(f"contact_sheet: --bg {args.bg!r} is not a colour (try '#808080' or 'checker')", file=sys.stderr)
        return 1

    images = []
    bad: List[str] = []
    for p in paths:
        try:
            with Image.open(p) as im:
                images.append(im.convert("RGBA"))
        except Exception as e:  # noqa: BLE001 - every unreadable file is reported, none guessed
            bad.append(f"{p} ({type(e).__name__})")
    if bad:
        print("contact_sheet: cannot read:\n  " + "\n  ".join(bad), file=sys.stderr)
        return 1

    max_w, max_h = args.cell
    fits = [min(max_w / im.width, max_h / im.height) for im in images]
    if args.same_scale:  # one factor for all: true relative sizes (two phones, icon sizes)
        fits = [min(fits)] * len(images)
    scaled = []
    for im, k in zip(images, fits):
        if k > 1 and not args.upscale:
            k = 1.0
        size = (max(1, round(im.width * k)), max(1, round(im.height * k)))
        if size != im.size:
            im = im.resize(size, Image.NEAREST if k > 1 else Image.LANCZOS)
        scaled.append(im)

    n = len(scaled)
    cols = n if args.filmstrip else (args.cols or math.ceil(math.sqrt(n)))
    cols = min(cols, n)
    rows = math.ceil(n / cols)
    gap = args.gap
    font = _font(ImageFont, 13)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    line_h = probe.textbbox((0, 0), "Ag", font=font)[3] + 4
    label_h = 0 if args.label == "none" else line_h
    cell_w = max(im.width for im in scaled)
    cell_h = max(im.height for im in scaled)
    if label_h:  # widen narrow cells for their labels, but never past the --cell width
        widest = max(probe.textlength(label_for(p, i, args.label), font=font) for i, p in enumerate(paths))
        cell_w = max(cell_w, min(max_w, math.ceil(widest)))
    title_h = 0 if not args.title else line_h + gap
    width = cols * cell_w + (cols + 1) * gap
    height = title_h + rows * (cell_h + label_h) + (rows + 1) * gap
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"contact_sheet: the sheet would be {width}x{height} px; use a smaller --cell, "
              "more --cols, or --every", file=sys.stderr)
        return 1

    sheet = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(sheet)
    ink = (0, 0, 0) if (bg[0] * 299 + bg[1] * 587 + bg[2] * 114) / 1000 > 140 else (255, 255, 255)
    if args.title:
        draw.text((gap, gap), _fit(args.title, draw, font, width - 2 * gap), fill=ink, font=font)
    for i, im in enumerate(scaled):
        r, c = divmod(i, cols)
        x0 = gap + c * (cell_w + gap)
        y0 = title_h + gap + r * (cell_h + label_h + gap)
        px = x0 + (cell_w - im.width) // 2
        py = y0 + (cell_h - im.height) // 2
        if checker:  # only under the image itself, so its own edges show against the margin
            square = 8
            for yy in range(0, im.height, square):
                for xx in range(0, im.width, square):
                    shade = (204, 204, 204) if (xx // square + yy // square) % 2 else (255, 255, 255)
                    draw.rectangle([px + xx, py + yy, px + min(xx + square, im.width) - 1,
                                    py + min(yy + square, im.height) - 1], fill=shade)
        sheet.paste(im, (px, py), im)
        if label_h:
            text = _fit(label_for(paths[i], i, args.label), draw, font, cell_w)
            tw = draw.textlength(text, font=font)
            draw.text((x0 + (cell_w - tw) / 2, y0 + cell_h + 2), text, fill=ink, font=font)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    shape = "filmstrip" if args.filmstrip else f"{cols}x{rows} grid"
    print(f"contact_sheet: wrote {args.out}: {n} images, {shape}, cell {cell_w}x{cell_h}, {width}x{height} px")
    return 0


# --------------------------------------------------------------------------------------------
# Selftest: images generated in a temp folder; every expected size and colour is a literal here.


def selftest() -> int:
    Image, _, _, _ = _pil()
    failures: List[str] = []
    count = 0
    script = str(Path(__file__).resolve())
    iso = ["-I"] if sys.flags.isolated else []  # a child must see the same Pillow as this process

    def case(label: str, ok: bool, detail: str = "") -> None:
        nonlocal count
        count += 1
        if ok:
            print(f"  ok  {label}")
        else:
            failures.append(label)
            print(f"FAIL  {label}: {detail}")

    def run(argv: Sequence[str]) -> Tuple[int, str, str]:
        proc = subprocess.run([sys.executable, *iso, script, *argv], capture_output=True, text=True)
        return proc.returncode, proc.stdout, proc.stderr

    def load(path):
        """The image at path as RGB with its file closed, or None if it was not written."""
        if not Path(path).is_file():
            return None
        with Image.open(path) as im:
            return im.convert("RGB")

    def at(img, xy):
        """The pixel at xy, or None when the sheet is missing or too small (a FAIL, not a crash)."""
        if img is None or not (0 <= xy[0] < img.width and 0 <= xy[1] < img.height):
            return None
        return img.getpixel(xy)

    def near(got, want: Tuple[int, int, int], tol: int = 2) -> bool:
        return got is not None and all(abs(g - w) <= tol for g, w in zip(got[:3], want))

    def size(img) -> Optional[Tuple[int, int]]:
        return None if img is None else img.size

    def pixels(img) -> List[Tuple[int, int, int]]:
        raw = img.convert("RGB").tobytes()
        return [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]

    grey = (128, 128, 128)
    with tempfile.TemporaryDirectory(prefix="contact_sheet_selftest_") as tmp_name:
        tmp = Path(tmp_name)
        src = tmp / "frames"
        src.mkdir()
        Image.new("RGB", (100, 50), (255, 0, 0)).save(src / "a.png")
        Image.new("RGBA", (50, 100), (0, 255, 0, 255)).save(src / "b.png")
        half = Image.new("RGBA", (80, 80), (0, 0, 255, 255))
        half.paste((0, 0, 0, 0), (0, 0, 40, 80))  # left half fully transparent
        half.save(src / "c.png")
        Image.new("RGB", (400, 200), (0, 255, 255)).save(src / "d.png")
        Image.new("RGB", (60, 40), (255, 255, 0)).save(src / "frame_2.png")
        Image.new("RGB", (60, 40), (255, 0, 255)).save(src / "frame_10.png")
        (tmp / "broken.png").write_text("not an image\n")
        Image.new("RGB", (10, 10), (10, 20, 30)).save(tmp / "tiny.png")
        (tmp / "no_pngs").mkdir()

        # Grid of a folder: natural order a, b, c, d, frame_2, frame_10; 3 columns.
        # Cells: widths 100, 50, 80, 100 (d 400x200 scaled to 100x50), 60, 60 -> 100;
        # heights 50, 100, 80, 50, 40, 40 -> 100. Sheet: 3*100 + 4*10 = 340 wide, 2*100 + 3*10 = 230 high.
        grid = tmp / "out" / "grid.png"
        rc, out, err = run([str(src), "--out", str(grid), "--cols", "3", "--cell", "100",
                            "--gap", "10", "--label", "none", "--bg", "#808080"])
        case("grid exits 0", rc == 0, f"rc={rc} {err!r}")
        sheet = load(grid)
        case("grid size is 340x230", size(sheet) == (340, 230), str(size(sheet)))
        case("cell 1 is a (red)", near(at(sheet, (60, 60)), (255, 0, 0)), str(at(sheet, (60, 60))))
        case("cell 2 is b (green)", near(at(sheet, (170, 60)), (0, 255, 0)), str(at(sheet, (170, 60))))
        case("transparent half shows the sheet colour", near(at(sheet, (250, 60)), grey), str(at(sheet, (250, 60))))
        case("opaque half is blue", near(at(sheet, (300, 60)), (0, 0, 255)), str(at(sheet, (300, 60))))
        case("large image scaled down into its cell (cyan)", near(at(sheet, (60, 170)), (0, 255, 255)),
             str(at(sheet, (60, 170))))
        case("natural order: frame_2 before frame_10", near(at(sheet, (170, 170)), (255, 255, 0))
             and near(at(sheet, (280, 170)), (255, 0, 255)), f"{at(sheet, (170, 170))} {at(sheet, (280, 170))}")
        case("gaps keep the sheet colour", near(at(sheet, (5, 5)), grey), str(at(sheet, (5, 5))))
        case("report names the shape", "6 images, 3x2 grid, cell 100x100, 340x230 px" in out, out)

        # Default columns: ceil(sqrt(6)) = 3, so the same size; -o works as --out.
        auto = tmp / "auto.png"
        rc, _, err = run([str(src), "-o", str(auto), "--cell", "100", "--gap", "10", "--label", "none"])
        case("default columns are ceil(sqrt(n)), -o accepted", rc == 0 and size(load(auto)) == (340, 230),
             f"rc={rc} {err!r}")

        # WxH cells: a (100x50) and b (50x100) in 60x120 cells -> a 60x30, b 50x100; cell 60x100.
        wxh = tmp / "wxh.png"
        rc, out, err = run([str(src / "a.png"), str(src / "b.png"), "--out", str(wxh), "--cell", "60x120",
                            "--gap", "0", "--label", "none"])
        case("WxH cell keeps a tall image tall (cell 60x100)", rc == 0 and "cell 60x100" in out
             and size(load(wxh)) == (120, 100), f"rc={rc} {out!r} {err!r}")

        # Labels add a strip under each row, with ink in it.
        lab = tmp / "labels.png"
        rc, _, err = run([str(src), "--out", str(lab), "--cols", "3", "--cell", "100", "--gap", "10"])
        labelled = load(lab)
        ok_lab = labelled is not None and labelled.size[0] == 340 and labelled.size[1] > 230
        case("labels make the sheet taller", rc == 0 and ok_lab, f"rc={rc} {size(labelled)} {err!r}")
        inked = sum(1 for p in pixels(labelled.crop((10, 110, 110, 122))) if not near(p, grey, 10)) if ok_lab else 0
        case("label strip has text in it", inked > 10, f"{inked} inked pixels")
        plain = sheet.crop((10, 110, 110, 120)) if size(sheet) == (340, 230) else None
        case("no labels means an empty gap", plain is not None and all(near(p, grey) for p in pixels(plain)))

        # Filmstrip keeps an explicit order: c, a, b in one row. Cell 100x100: 340 x 120.
        film = tmp / "film.png"
        rc, _, _ = run([str(src / "c.png"), str(src / "a.png"), str(src / "b.png"), "--out", str(film),
                        "--filmstrip", "--cell", "100", "--gap", "10", "--label", "none"])
        strip = load(film)
        case("filmstrip is one row, 340x120", rc == 0 and size(strip) == (340, 120), f"rc={rc} {size(strip)}")
        case("filmstrip keeps the given order (c first)", near(at(strip, (80, 60)), (0, 0, 255))
             and near(at(strip, (170, 60)), (255, 0, 0)), str(at(strip, (80, 60))))

        # Checker shows transparency as a checkerboard, but only inside the image's own rectangle.
        chk = tmp / "checker.png"
        rc, _, _ = run([str(src / "c.png"), "--out", str(chk), "--cell", "100", "--gap", "10",
                        "--label", "none", "--bg", "checker"])
        cimg = load(chk)
        shades = {at(cimg, (x, 40)) for x in range(12, 48)} if size(cimg) == (100, 100) else set()
        case("checker behind transparency", rc == 0 and shades == {(255, 255, 255), (204, 204, 204)}, str(shades))
        chk2 = tmp / "checker2.png"
        rc, _, _ = run([str(src / "a.png"), str(src / "b.png"), "--out", str(chk2), "--cell", "100", "--gap", "10",
                        "--label", "none", "--bg", "checker"])
        c2 = load(chk2)  # 2 columns of 100x100 cells: a sits at y 35..84 in its cell, b at x 145..194
        case("checker stays off the cell margin", rc == 0 and size(c2) == (230, 120)
             and near(at(c2, (60, 20)), grey) and near(at(c2, (130, 60)), grey)
             and near(at(c2, (60, 60)), (255, 0, 0)), f"{size(c2)} {at(c2, (60, 20))} {at(c2, (130, 60))}")

        # Small images stay small unless --upscale.
        small = tmp / "small.png"
        rc, _, _ = run([str(tmp / "tiny.png"), "--out", str(small), "--cell", "100", "--gap", "0", "--label", "none"])
        case("never upscaled by default (10x10)", rc == 0 and size(load(small)) == (10, 10), str(size(load(small))))
        big = tmp / "big.png"
        rc, _, _ = run([str(tmp / "tiny.png"), "--out", str(big), "--cell", "100", "--gap", "0",
                        "--label", "none", "--upscale"])
        case("--upscale fills the cell (100x100)", rc == 0 and size(load(big)) == (100, 100), str(size(load(big))))

        # --same-scale: a (100x50) and d (400x200) in 200 px cells. d needs 0.5, so a becomes 50x25
        # (not its own 100x50). Cells 200x100, 2 columns: 2*200 + 3*10 = 430 by 100 + 20 = 120.
        same = tmp / "same.png"
        rc, _, err = run([str(src / "a.png"), str(src / "d.png"), "--out", str(same), "--cell", "200",
                          "--gap", "10", "--label", "none", "--same-scale"])
        simg = load(same)
        case("--same-scale sheet is 430x120", rc == 0 and size(simg) == (430, 120), f"rc={rc} {size(simg)} {err!r}")
        case("--same-scale keeps relative size (a is 50 wide)", near(at(simg, (110, 60)), (255, 0, 0))
             and near(at(simg, (70, 60)), grey), f"{at(simg, (70, 60))}")

        # Labels widen a narrow cell up to the --cell width, so they are not cut needlessly.
        wide = tmp / "wide.png"
        long_name = tmp / "a_label_much_wider_than_fifty_pixels.png"   # a 50x100 image
        Image.new("RGB", (50, 100), (0, 255, 0)).save(long_name)
        rc, _, _ = run([str(long_name), "--out", str(wide), "--cell", "200", "--gap", "0", "--label", "name"])
        wsize = size(load(wide))
        case("a label widens a 50 px cell (but not past 200)", rc == 0 and wsize is not None
             and 50 < wsize[0] <= 200, str(wsize))

        # --every 2 keeps a, c, frame_2: one row of 3 at --cols 3.
        ev = tmp / "every.png"
        rc, out, _ = run([str(src), "--out", str(ev), "--cols", "3", "--cell", "100", "--gap", "10",
                          "--label", "none", "--every", "2"])
        case("--every 2 keeps 3 of 6", rc == 0 and "3 images" in out, out)

        # Inputs that are missing or match nothing fail loudly; --allow-empty skips only globs and folders.
        x = str(tmp / "x.png")
        rc, _, err = run([str(src / "a.png"), str(tmp / "does_not_exist.png"), "--out", x])
        case("a missing file is exit 2, named, nothing written", rc == 2 and "does_not_exist.png" in err
             and not Path(x).exists(), f"rc={rc} {err!r}")
        rc, _, err = run([str(src / "a.png"), str(tmp / "nothing_*.png"), "--out", x])
        case("a glob that matches nothing is exit 2", rc == 2 and "matched nothing" in err, f"rc={rc} {err!r}")
        rc, _, err = run([str(src / "a.png"), str(tmp / "no_pngs"), "--out", x])
        case("a folder with no PNG is exit 2", rc == 2 and "no_pngs" in err, f"rc={rc} {err!r}")
        rc, out, err = run([str(src / "a.png"), str(tmp / "nothing_*.png"), "--out", x, "--allow-empty"])
        case("--allow-empty skips an empty glob with a note", rc == 0 and "1 images" in out
             and "skipped" in err, f"rc={rc} {err!r}")
        rc, _, err = run([str(tmp / "missing.png"), "--out", x, "--allow-empty"])
        case("--allow-empty never excuses a missing file", rc == 2 and "missing.png" in err, f"rc={rc} {err!r}")
        rc, _, err = run([str(tmp / "nothing_*.png"), "--out", x, "--allow-empty"])
        case("nothing left to tile is exit 2", rc == 2 and "no images to tile" in err, f"rc={rc} {err!r}")

        # Other failures, each for its own reason.
        rc, _, err = run([str(tmp / "broken.png"), "--out", x])
        case("unreadable file named, exit 1", rc == 1 and "broken.png" in err, f"rc={rc} {err!r}")
        rc, _, err = run([str(src / "a.png"), "--out", str(src / "a.png")])
        case("refuses to overwrite an input", rc == 1 and "is also an input" in err, f"rc={rc} {err!r}")
        rc, _, err = run([str(src / "a.png"), "--out", x, "--bg", "not-a-colour"])
        case("bad colour refused", rc == 1 and "is not a colour" in err, f"rc={rc} {err!r}")
        rc, _, err = run([str(src / "a.png"), "--out", x, "--cell", "0"])
        case("tiny cell refused", rc != 0 and "--cell" in err, f"rc={rc} {err!r}")

        # Missing Pillow: a clear install message, exit 1 (PIL blocked in a child interpreter).
        blocker = ("import sys, runpy; sys.modules['PIL'] = None; "
                   f"sys.argv = ['contact_sheet.py', {str(src / 'a.png')!r}, '--out', {x!r}]; "
                   f"runpy.run_path({script!r}, run_name='__main__')")
        proc = subprocess.run([sys.executable, *iso, "-c", blocker], capture_output=True, text=True)
        case("missing Pillow explains the venv install", proc.returncode == 1 and "needs Pillow" in proc.stderr
             and "pip install pillow" in proc.stderr, f"rc={proc.returncode} {proc.stderr!r}")

    print(f"contact_sheet selftest: {count} cases, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
