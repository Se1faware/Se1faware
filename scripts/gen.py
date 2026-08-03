#!/usr/bin/env python3
"""Generate black-white pixel GIFs + ASCII logo for Se1faware profile README.

v2: 2x finer grain (SCALE=4, double-resolution sprites), new skills.gif.
"""
import os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
os.makedirs(ASSETS, exist_ok=True)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCALE = 4


def save_gif(frames, name, duration):
    frames[0].save(
        os.path.join(ASSETS, name),
        save_all=True, append_images=frames[1:],
        duration=duration, loop=0, disposal=2,
    )
    print("wrote", name, f"{len(frames)} frames x{duration}ms")


def canvas(w, h):
    img = Image.new("RGB", (w, h), WHITE)
    return img, img.load()


def put(px, w, h, x, y):
    if 0 <= x < w and 0 <= y < h:
        px[x, y] = BLACK


def scale(img, factor=SCALE):
    return img.resize((img.width * factor, img.height * factor), Image.Resampling.NEAREST)


# ---------------------------------------------------------------------------
# hero.gif — 照镜子的时候,倒影先动了 (80x48, fine grain)
# ---------------------------------------------------------------------------
def person_pixels(arm="down", blink=False):
    p = set()
    # head (6,0)-(17,9); eyes = white 2x2 gaps
    for y in range(10):
        for x in range(6, 18):
            if not blink and y in (4, 5) and (9 <= x <= 10 or 15 <= x <= 16):
                continue
            p.add((x, y))
    # neck (10,10)-(13,12)
    for y in range(10, 13):
        for x in range(10, 14):
            p.add((x, y))
    # torso (5,11)-(17,23)
    for y in range(11, 24):
        for x in range(5, 18):
            p.add((x, y))
    # arm: 4px wide, 1px gap from torso (col 18)
    # down = hanging beside body (y14-23), wave = raised beside head (y0-11)
    if arm == "down":
        for y in range(14, 24):
            for x in range(19, 23):
                p.add((x, y))
    else:
        for y in range(0, 12):
            for x in range(19, 23):
                p.add((x, y))
    # legs (8-11,24-27) & (15-18,24-27)
    for y in range(24, 28):
        for x in range(8, 12):
            p.add((x, y))
        for x in range(15, 19):
            p.add((x, y))
    # feet row 28: (6-11) & (15-20)
    for x in range(6, 12):
        p.add((x, 28))
    for x in range(15, 21):
        p.add((x, 28))
    return p


def draw_hero(frame):
    w, h = 80, 48
    img, px = canvas(w, h)
    # ground
    for x in range(w):
        put(px, w, h, x, 42)
    # dashed mirror at x=40
    for y in range(0, 43, 2):
        put(px, w, h, 40, y)
    real = person_pixels("down", blink=(frame == 2))
    refl = person_pixels("wave" if frame in (1, 2) else "down")
    for sx, sy in real:
        put(px, w, h, sx + 4, sy + 13)
    for sx, sy in refl:
        put(px, w, h, 53 + (27 - (sx + 4)), sy + 13)
    return img


# ---------------------------------------------------------------------------
# heart.gif — 心还在跳 (30x28, 2x of an 11x9 heart)
# ---------------------------------------------------------------------------
HEART = [
    ".###...###.",
    "#...#.#...#",
    "#....#....#",
    "#.........#",
    "..#.....#..",
    "...#...#...",
    "....#.#....",
    ".....#.....",
]


def draw_heart(pulse):
    w, h = 30, 28
    img, px = canvas(w, h)
    rows = HEART + ([".....#....."] if pulse else [])
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                for dy in (0, 1):
                    for dx in (0, 1):
                        put(px, w, h, 4 + x * 2 + dx, 4 + y * 2 + dy)
    return img


# ---------------------------------------------------------------------------
# skills.gif — 拆解 · 构建 · 觉察 · 行动 + 观象→构序→观心→见性 (132x52)
# ---------------------------------------------------------------------------
FONT = {
    "S": ["█████", "█....", "█████", "....█", "█████"],
    "E": ["█████", "█....", "████.", "█....", "█████"],
    "1": [".██..", "█.█..", "..█..", "..█..", "█████"],
    "F": ["█████", "█....", "████.", "█....", "█...."],
    "A": ["..█..", ".█.█.", "█████", "█...█", "█...█"],
    "W": ["█...█", "█...█", "█.█.█", "██.██", "█...█"],
    "R": ["████.", "█...█", "████.", "█..█.", "█...█"],
    "P": ["████.", "█...█", "████.", "█....", "█...."],
    "L": ["█....", "█....", "█....", "█....", "█████"],
    "I": ["█████", "..█..", "..█..", "..█..", "█████"],
    "T": ["█████", "..█..", "..█..", "..█..", "..█.."],
    "B": ["████.", "█...█", "████.", "█...█", "████."],
    "U": ["█...█", "█...█", "█...█", "█...█", "█████"],
    "D": ["████.", "█...█", "█...█", "█...█", "████."],
    "C": ["█████", "█....", "█....", "█....", "█████"],
    "Y": ["█...█", "█...█", ".█.█.", "..█..", "..█.."],
    "K": ["█...█", "█..█.", "███..", "█..█.", "█...█"],
    "N": ["█...█", "██..█", "█.█.█", "█..██", "█...█"],
    "G": [".████", "█....", "█..██", "█...█", ".████"],
    "H": ["█...█", "█...█", "█████", "█...█", "█...█"],
    "O": ["█████", "█...█", "█...█", "█...█", "█████"],
    "M": ["█...█", "██.██", "█.█.█", "█...█", "█...█"],
    " ": [".....", ".....", ".....", ".....", "....."],
    "·": [".....", "..█..", "..█..", "..█..", "....."],
}

PANEL_W = 44
ICON_Y = 4
LABEL_Y = 40


def draw_label(px, w, h, panel_x, text):
    glyphs = [FONT[c] for c in text]
    tw = len(text) * 6 - 1  # 5px per char + 1px gap
    ox = panel_x + (PANEL_W - tw) // 2
    for gi, g in enumerate(glyphs):
        for ry, row in enumerate(g):
            for rx, ch in enumerate(row):
                if ch == "█":
                    put(px, w, h, ox + gi * 6 + rx, LABEL_Y + ry)


def box(px, w, h, ox, oy, x1, y1, x2, y2):
    for x in range(x1, x2 + 1):
        put(px, w, h, ox + x, oy + y1)
        put(px, w, h, ox + x, oy + y2)
    for y in range(y1, y2 + 1):
        put(px, w, h, ox + x1, oy + y)
        put(px, w, h, ox + x2, oy + y)


def fill(px, w, h, ox, oy, x1, y1, x2, y2):
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            put(px, w, h, ox + x, oy + y)


def hline(px, w, h, ox, oy, x1, x2, y):
    for x in range(x1, x2 + 1):
        put(px, w, h, ox + x, oy + y)


def vline(px, w, h, ox, oy, x, y1, y2):
    for y in range(y1, y2 + 1):
        put(px, w, h, ox + x, oy + y)


def icon_split(px, w, h, ox, oy, frame):
    # a gridded block; one unit cracks out and flies away
    box(px, w, h, ox, oy, 4, 6, 23, 25)
    vline(px, w, h, ox, oy, 13, 7, 24)
    vline(px, w, h, ox, oy, 14, 7, 24)
    hline(px, w, h, ox, oy, 5, 22, 15)
    hline(px, w, h, ox, oy, 5, 22, 16)
    dx, dy = (1, -1) if frame == 0 else (5, -5)
    box(px, w, h, ox, oy, 14 + dx, 6 + dy, 23 + dx, 14 + dy)
    fill(px, w, h, ox, oy, 16 + dx, 9 + dy, 21 + dx, 11 + dy)


def icon_build(px, w, h, ox, oy, frame):
    # three stacked layers; a block drops into place
    hline(px, w, h, ox, oy, 4, 27, 27)  # ground
    box(px, w, h, ox, oy, 5, 22, 26, 26)
    hline(px, w, h, ox, oy, 6, 25, 24)
    box(px, w, h, ox, oy, 9, 17, 22, 21)
    hline(px, w, h, ox, oy, 10, 21, 19)
    box(px, w, h, ox, oy, 12, 12, 19, 16)
    hline(px, w, h, ox, oy, 13, 18, 14)
    fy = 3 if frame == 0 else 8  # falling block
    box(px, w, h, ox, oy, 14, fy, 17, fy + 3)


def icon_see(px, w, h, ox, oy, frame):
    # an eye whose pupil holds a tiny self — gaze shifts side to side
    dx = 2 if frame == 1 else 0
    hline(px, w, h, ox, oy, 11, 20, 9)   # upper lid
    hline(px, w, h, ox, oy, 9, 22, 10)
    hline(px, w, h, ox, oy, 8, 23, 11)
    hline(px, w, h, ox, oy, 7, 24, 12)
    vline(px, w, h, ox, oy, 7, 12, 19)   # eye corners
    vline(px, w, h, ox, oy, 24, 12, 19)
    hline(px, w, h, ox, oy, 8, 23, 19)   # lower lid
    hline(px, w, h, ox, oy, 9, 22, 20)
    hline(px, w, h, ox, oy, 11, 20, 21)
    put(px, w, h, ox + 12, oy + 8)       # lashes
    put(px, w, h, ox + 16, oy + 8)
    put(px, w, h, ox + 19, oy + 8)
    # pupil (black) minus highlight and the tiny self (both stay white)
    for y in range(13, 19):
        x1, x2 = (13 + dx, 18 + dx) if y in (13, 18) else (11 + dx, 20 + dx)
        for x in range(x1, x2 + 1):
            if 12 + dx <= x <= 13 + dx and y in (13, 14):
                continue  # highlight
            if 15 + dx <= x <= 16 + dx and 14 <= y <= 18:
                continue  # the self inside the pupil
            put(px, w, h, ox + x, oy + y)


def icon_act(px, w, h, ox, oy, frame):
    # a running figure: legs alternate, speed lines drift
    hline(px, w, h, ox, oy, 6, 26, 24)   # ground
    hline(px, w, h, ox, oy, 15, 18, 5)   # head
    vline(px, w, h, ox, oy, 14, 6, 8)
    vline(px, w, h, ox, oy, 19, 6, 8)
    hline(px, w, h, ox, oy, 15, 18, 9)
    put(px, w, h, ox + 16, oy + 7)       # eye
    for y in range(10, 17):              # leaning torso
        hline(px, w, h, ox, oy, 15, 21, y)
    if frame == 0:                       # arms
        vline(px, w, h, ox, oy, 22, 10, 13)
        vline(px, w, h, ox, oy, 13, 11, 14)
    else:
        vline(px, w, h, ox, oy, 13, 10, 13)
        vline(px, w, h, ox, oy, 22, 11, 14)
    if frame == 0:                       # legs: diagonal stride
        for x, y in ((19, 17), (20, 18), (21, 19), (22, 20), (23, 21), (23, 22), (23, 23)):
            put(px, w, h, ox + x, oy + y)  # front leg forward
        for x, y in ((14, 17), (13, 18), (12, 19), (11, 20), (10, 21), (10, 22), (10, 23)):
            put(px, w, h, ox + x, oy + y)  # back leg kicking
    else:
        for x, y in ((20, 17), (21, 18), (22, 19), (23, 20), (24, 21), (24, 22), (24, 23)):
            put(px, w, h, ox + x, oy + y)  # front leg further
        for x, y in ((13, 17), (12, 18), (11, 19), (10, 20), (9, 21), (9, 22), (9, 23)):
            put(px, w, h, ox + x, oy + y)  # back leg further
    if frame == 0:                       # speed lines
        hline(px, w, h, ox, oy, 3, 5, 12)
        hline(px, w, h, ox, oy, 4, 6, 16)
        hline(px, w, h, ox, oy, 3, 4, 20)
    else:
        hline(px, w, h, ox, oy, 4, 6, 12)
        hline(px, w, h, ox, oy, 5, 7, 16)
        hline(px, w, h, ox, oy, 4, 5, 20)


def draw_skills(frame):
    # 180x48: four 32px animated icons + pixel labels (SCALE 3 -> 540x144)
    w, h = 180, 48
    img, px = canvas(w, h)
    panels = [
        (2, "SPLIT", lambda o: icon_split(px, w, h, o, ICON_Y, frame)),
        (46, "BUILD", lambda o: icon_build(px, w, h, o, ICON_Y, frame)),
        (90, "SEE", lambda o: icon_see(px, w, h, o, ICON_Y, frame)),
        (134, "ACT", lambda o: icon_act(px, w, h, o, ICON_Y, frame)),
    ]
    for p, label, draw in panels:
        draw(p)
        draw_label(px, w, h, p, label)
    return img


# ---------------------------------------------------------------------------
# dev-icons.gif — 608x64 long strip, 6 x 48px animated icons, space-between
# BTC coin flip / bot face / taiji spin / code brackets / gear / blocks
# ---------------------------------------------------------------------------
def icon_btc(px, w, h, ox, oy, frame):
    c = 24
    narrow = frame % 2 == 1
    for y in range(48):
        for x in range(48):
            dx, dy = x - c, y - c
            ex = dx * 2 if narrow else dx
            d2 = ex * ex + dy * dy
            if 361 <= d2 <= 441:                    # outer ring r19-21
                put(px, w, h, ox + x, oy + y)
            elif not narrow and 156 <= d2 <= 169:   # inner ring r12.5-13
                put(px, w, h, ox + x, oy + y)
    if narrow:
        vline(px, w, h, ox, oy, 24, 19, 29)         # slim ₿ while flipping
    else:
        vline(px, w, h, ox, oy, 24, 17, 31)
        hline(px, w, h, ox, oy, 20, 24, 18)
        hline(px, w, h, ox, oy, 20, 24, 20)
        hline(px, w, h, ox, oy, 20, 24, 28)
        hline(px, w, h, ox, oy, 20, 24, 30)
    fill(px, w, h, ox, oy, 22, 2, 25, 3)            # cardinal ticks
    fill(px, w, h, ox, oy, 44, 22, 45, 25)
    fill(px, w, h, ox, oy, 22, 44, 25, 45)
    fill(px, w, h, ox, oy, 2, 22, 3, 25)


def icon_bot(px, w, h, ox, oy, frame):
    blink = frame == 2
    fill(px, w, h, ox, oy, 22, 3, 26, 5)            # antenna bulb
    if blink:
        fill(px, w, h, ox, oy, 24, 4, 24, 4)        # light off
    vline(px, w, h, ox, oy, 24, 6, 10)
    fill(px, w, h, ox, oy, 7, 17, 8, 24)            # side ears
    fill(px, w, h, ox, oy, 39, 17, 40, 24)
    for y in range(10, 36):                          # rounded head frame
        for x in range(11, 37):
            corner = (x in (11, 36) and y in (10, 35))
            if (x in (11, 36) or y in (10, 35)) and not corner:
                put(px, w, h, ox + x, oy + y)
    if blink:                                        # eyes -> closed lines
        hline(px, w, h, ox, oy, 18, 20, 20)
        hline(px, w, h, ox, oy, 27, 29, 20)
    else:                                            # 3x4 eyes + highlight
        for y in range(18, 22):
            for x in range(18, 21):
                if not (x == 18 and y == 18):
                    put(px, w, h, ox + x, oy + y)
            for x in range(27, 30):
                if not (x == 27 and y == 18):
                    put(px, w, h, ox + x, oy + y)
    fill(px, w, h, ox, oy, 21, 28, 26, 29)           # mouth


def icon_taiji(px, w, h, ox, oy, frame):
    c = 24
    reverse = frame % 2 == 1
    for y in range(48):
        for x in range(48):
            dx, dy = x - c, y - c
            d2 = dx * dx + dy * dy
            if 361 <= d2 <= 441:                     # ring r19-21
                put(px, w, h, ox + x, oy + y)
                continue
            if d2 > 400:
                continue
            in_left = x < 24
            black = in_left != reverse
            if not reverse:                          # eyes swap on flip
                white_eye = 19 <= x <= 22 and 9 <= y <= 12
                black_eye = 26 <= x <= 29 and 36 <= y <= 39
            else:
                white_eye = 26 <= x <= 29 and 9 <= y <= 12
                black_eye = 19 <= x <= 22 and 36 <= y <= 39
            if (black and not white_eye) or black_eye:
                put(px, w, h, ox + x, oy + y)


def icon_code(px, w, h, ox, oy, frame):
    for i in range(12):                              # 2px brackets
        for t in range(2):
            put(px, w, h, ox + 20 - i, oy + 12 + i + t)
            put(px, w, h, ox + 20 - i + t, oy + 12 + i)
            put(px, w, h, ox + 20 - i, oy + 36 - i - t)
            put(px, w, h, ox + 20 - i + t, oy + 36 - i)
            put(px, w, h, ox + 28 + i, oy + 12 + i + t)
            put(px, w, h, ox + 28 + i - t, oy + 12 + i)
            put(px, w, h, ox + 28 + i, oy + 36 - i - t)
            put(px, w, h, ox + 28 + i - t, oy + 36 - i)
    if frame % 2 == 0:                               # slash / vs \
        for i in range(10):
            put(px, w, h, ox + 23 + i, oy + 14 + i)
            put(px, w, h, ox + 24 + i, oy + 14 + i)
        hline(px, w, h, ox, oy, 17, 31, 41)          # cursor blink
    else:
        for i in range(10):
            put(px, w, h, ox + 32 - i, oy + 14 + i)
            put(px, w, h, ox + 31 - i, oy + 14 + i)


def icon_gear(px, w, h, ox, oy, frame):
    c = 24
    diag = frame % 2 == 1
    for y in range(48):
        for x in range(48):
            dx, dy = x - c, y - c
            d2 = dx * dx + dy * dy
            if 289 <= d2 <= 361:                     # outer ring r17-19
                put(px, w, h, ox + x, oy + y)
            elif 81 <= d2 <= 121:                    # inner ring r9-11
                put(px, w, h, ox + x, oy + y)
    if not diag:
        fill(px, w, h, ox, oy, 22, 1, 25, 4)         # N E S W teeth
        fill(px, w, h, ox, oy, 43, 22, 46, 25)
        fill(px, w, h, ox, oy, 22, 43, 25, 46)
        fill(px, w, h, ox, oy, 1, 22, 4, 25)
        vline(px, w, h, ox, oy, 24, 12, 18)          # cardinal spokes
        vline(px, w, h, ox, oy, 24, 29, 35)
        hline(px, w, h, ox, oy, 12, 18, 24)
        hline(px, w, h, ox, oy, 29, 35, 24)
    else:
        fill(px, w, h, ox, oy, 32, 4, 35, 7)         # diagonal teeth
        fill(px, w, h, ox, oy, 40, 32, 43, 35)
        fill(px, w, h, ox, oy, 12, 40, 15, 43)
        fill(px, w, h, ox, oy, 4, 12, 7, 15)
        for i in range(6):                           # diagonal spokes
            put(px, w, h, ox + 24 + i, oy + 12 + i)
            put(px, w, h, ox + 24 - i, oy + 12 + i)
            put(px, w, h, ox + 24 + i, oy + 36 - i)
            put(px, w, h, ox + 24 - i, oy + 36 - i)


def icon_blocks(px, w, h, ox, oy, frame):
    hline(px, w, h, ox, oy, 8, 39, 42)               # ground
    fill(px, w, h, ox, oy, 10, 35, 37, 41)           # base layer
    fill(px, w, h, ox, oy, 14, 27, 33, 34)           # mid layer
    fill(px, w, h, ox, oy, 18, 19, 29, 26)           # top layer
    fy = 6 if frame % 2 == 0 else 10
    box(px, w, h, ox, oy, 21, fy, 26, fy + 5)        # falling block
    if frame % 2 == 0:
        put(px, w, h, ox + 23, oy + 3)               # drop trails
        put(px, w, h, ox + 24, oy + 4)


def draw_dev_icons(frame):
    w, h = 608, 64
    img, px = canvas(w, h)
    for i, fn in enumerate((
        lambda o: icon_btc(px, w, h, o, 8, frame),
        lambda o: icon_bot(px, w, h, o, 8, frame),
        lambda o: icon_taiji(px, w, h, o, 8, frame),
        lambda o: icon_code(px, w, h, o, 8, frame),
        lambda o: icon_gear(px, w, h, o, 8, frame),
        lambda o: icon_blocks(px, w, h, o, 8, frame),
    )):
        fn(i * 112)  # 48px icon + 64px gap, first flush-left, last flush-right
    return img


# ---------------------------------------------------------------------------
# tagline.png — STAY AWARE · KEEP BUILDING (77x15 pixel-font subtitle)
# ---------------------------------------------------------------------------
def draw_tagline():
    w, h = 77, 15
    img, px = canvas(w, h)

    def put_text(line, y):
        glyphs = [FONT[c] for c in line]
        tw = len(line) * 6 - 1
        ox = (w - tw) // 2
        for gi, g in enumerate(glyphs):
            for ry, row in enumerate(g):
                for rx, ch in enumerate(row):
                    if ch == "█":
                        put(px, w, h, ox + gi * 6 + rx, y + ry)

    put_text("STAY AWARE", 0)
    for ry in range(3):  # middle dot
        put(px, w, h, w // 2, 6 + ry)
    put_text("KEEP BUILDING", 10)
    return img


def save_png_both(name, img):
    img.save(os.path.join(ASSETS, name))
    ImageOps.invert(img).save(os.path.join(ASSETS, name.replace(".png", "-dark.png")))


# ---------------------------------------------------------------------------
# section headings — pixel-font titles (no GitHub h1 border possible)
# ---------------------------------------------------------------------------
def draw_heading(text):
    glyphs = [FONT[c] for c in text]
    tw = len(text) * 6 - 1
    w, h = tw + 8, 13  # 4px margins each side
    img, px = canvas(w, h)
    for gi, g in enumerate(glyphs):
        for ry, row in enumerate(g):
            for rx, ch in enumerate(row):
                if ch == "█":
                    put(px, w, h, 4 + gi * 6 + rx, 4 + ry)
    return img


# ---------------------------------------------------------------------------
# ASCII logo — SE1FAWARE
# ---------------------------------------------------------------------------
def ascii_logo(text="SE1FAWARE"):
    lines = [""] * 5
    for ch in text:
        glyph = FONT[ch]
        for i in range(5):
            lines[i] += glyph[i] + "  "
    return "\n".join(line.rstrip() for line in lines)


def save_both(name, frames, duration):
    """Save light (black-on-white) + dark (white-on-black) variants."""
    save_gif(frames, name, duration)
    save_gif([ImageOps.invert(f) for f in frames], name.replace(".gif", "-dark.gif"), duration)


if __name__ == "__main__":
    save_both("hero.gif", [scale(draw_hero(i)) for i in range(4)], 400)
    save_both("skills.gif", [scale(draw_skills(i), 3) for i in range(2)], 600)
    save_both("dev-icons.gif", [scale(draw_dev_icons(i)) for i in range(4)], 400)
    save_both("heart.gif", [scale(draw_heart(p)) for p in (False, True, False, True)], 240)
    save_png_both("tagline.png", scale(draw_tagline()))
    save_png_both("heading-whoami.png", scale(draw_heading("WHOAMI")))
    save_png_both("heading-how-i-work.png", scale(draw_heading("HOW I WORK")))
    save_png_both("heading-now-building.png", scale(draw_heading("NOW BUILDING")))

    print()
    print(ascii_logo())
