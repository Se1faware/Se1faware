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


def scale(img):
    return img.resize((img.width * SCALE, img.height * SCALE), Image.Resampling.NEAREST)


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
    " ": [".....", ".....", ".....", ".....", "....."],
    "·": [".....", "..█..", "..█..", "..█..", "....."],
}

PANEL_W = 32
ICON_X, ICON_Y = 6, 2
ICON_S = 20
LABEL_Y = 24


def draw_label(px, w, h, panel_x, text):
    glyphs = [FONT[c] for c in text]
    tw = len(text) * 6 - 1  # 5px per char + 1px gap
    ox = panel_x + (PANEL_W - tw) // 2
    for gi, g in enumerate(glyphs):
        for ry, row in enumerate(g):
            for rx, ch in enumerate(row):
                if ch == "█":
                    put(px, w, h, ox + gi * 6 + rx, LABEL_Y + ry)


def icon_split(px, w, h, ox, oy, apart):
    # a box splitting in two
    if not apart:
        for y in range(2, 18):
            for x in range(2, 18):
                if x in (2, 17) or y in (2, 17) or x in (9, 10):
                    put(px, w, h, ox + x, oy + y)
    else:
        for y in range(2, 18):
            for x in range(2, 9):
                if x in (2, 8) or y in (2, 17):
                    put(px, w, h, ox + x, oy + y)
            for x in range(11, 18):
                if x in (11, 17) or y in (2, 17):
                    put(px, w, h, ox + x, oy + y)


def icon_build(px, w, h, ox, oy, blink):
    # house: roof triangle + walls + door + window
    for y, xs in zip(range(2, 6), (range(7, 13), range(6, 14), range(5, 15), range(4, 16))):
        for x in xs:
            put(px, w, h, ox + x, oy + y)
    for x in range(3, 17):
        put(px, w, h, ox + x, oy + 6)   # wall top
        put(px, w, h, ox + x, oy + 17)  # wall bottom
    for y in range(6, 18):
        put(px, w, h, ox + 3, oy + y)
        put(px, w, h, ox + 16, oy + y)
    for x in range(8, 12):              # door (filled)
        for y in range(11, 18):
            put(px, w, h, ox + x, oy + y)
    for x in range(5, 8):               # window
        for y in range(8, 11):
            if blink:
                if x in (5, 7) or y in (8, 10):
                    put(px, w, h, ox + x, oy + y)
            else:
                put(px, w, h, ox + x, oy + y)


def icon_see(px, w, h, ox, oy, shift):
    # eye outline + darting pupil
    for y, xs in zip(range(7, 13), (range(5, 15), range(3, 17), range(3, 17), range(4, 16), range(7, 13), range(9, 11))):
        for x in xs:
            put(px, w, h, ox + x, oy + y)
    pupil_x = 9 + shift
    for x in range(pupil_x, pupil_x + 2):
        for y in range(8, 10):
            put(px, w, h, ox + x, oy + y)


def icon_act(px, w, h, ox, oy, move):
    # block arrow + motion dashes
    for y in range(8, 12):
        for x in range(2, 14):
            put(px, w, h, ox + x, oy + y)
    for y, xs in zip((6, 7, 12, 13), (range(15, 16), range(14, 17), range(14, 17), range(15, 16))):
        for x in xs:
            put(px, w, h, ox + x, oy + y)
    for yy, xx in ((16, 4), (18, 9)):
        for x in range(xx + move, xx + 3 + move):
            put(px, w, h, ox + x, oy + yy)


def draw_skills(frame):
    # 132x52: 4 animated icons + pixel labels on top, 观象→构序→观心→见性
    # squares row below (fill 1->2->3->4). Icons flip state every frame.
    w, h = 132, 52
    img, px = canvas(w, h)
    icon_state = frame % 2
    lit = frame + 1
    panels = [
        (2, "SPLIT", lambda o: icon_split(px, w, h, o, ICON_Y, apart=(icon_state == 1))),
        (34, "BUILD", lambda o: icon_build(px, w, h, o, ICON_Y, blink=(icon_state == 1))),
        (66, "SEE", lambda o: icon_see(px, w, h, o, ICON_Y, shift=(1 if icon_state == 1 else 0))),
        (98, "ACT", lambda o: icon_act(px, w, h, o, ICON_Y, move=(2 if icon_state == 1 else 0))),
    ]
    for p, label, draw in panels:
        draw(p)
        draw_label(px, w, h, p, label)
    # phases squares row, aligned under each panel
    for ox, oy in [(2, 34), (24, 34), (46, 34), (68, 34)][:lit]:
        for x in range(ox, ox + 16):
            for y in range(oy, oy + 16):
                put(px, w, h, x, y)
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
    save_both("skills.gif", [scale(draw_skills(i)) for i in range(4)], [300, 300, 300, 1200])
    save_both("heart.gif", [scale(draw_heart(p)) for p in (False, True, False, True)], 240)
    save_png_both("tagline.png", scale(draw_tagline()))

    print()
    print(ascii_logo())
