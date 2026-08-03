#!/usr/bin/env python3
"""Generate black-white pixel GIFs + ASCII logo for Se1faware profile README."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
os.makedirs(ASSETS, exist_ok=True)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCALE = 8


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


# ---------------------------------------------------------------------------
# hero.gif — 照镜子的时候,倒影先动了
# 40x24: real person | mirror | reflection (mirrored person)
# ---------------------------------------------------------------------------
def person_pixels(arm="down", blink=False):
    p = set()
    # head (2,0)-(7,3), eyes = white gaps at (3,2),(6,2)
    for y in range(4):
        for x in range(2, 8):
            if y == 2 and x in (3, 6) and not blink:
                continue
            p.add((x, y))
    # torso (1,4)-(8,9)
    for y in range(4, 10):
        for x in range(1, 9):
            p.add((x, y))
    # arm: outside the torso (1px gap)
    # down = single column hanging beside body (y 8-12)
    # wave = 2px-wide bar raised from shoulder to above head (y 0-6)
    if arm == "down":
        for y in range(8, 13):
            p.add((10, y))
    else:
        for y in range(0, 7):
            for x in (9, 10):
                p.add((x, y))
    # legs (2-3,10-12) & (6-7,10-12)
    for y in range(10, 13):
        for x in range(2, 4):
            p.add((x, y))
        for x in range(6, 8):
            p.add((x, y))
    # feet
    for x in range(1, 4):
        p.add((x, 13))
    for x in range(6, 9):
        p.add((x, 13))
    return p


def draw_hero(frame):
    w, h = 40, 24
    img, px = canvas(w, h)
    # ground
    for x in range(w):
        put(px, w, h, x, 21)
    # dashed mirror at x=20
    for y in range(0, 22, 2):
        put(px, w, h, 20, y)
    # real person at offset (2,8) — feet land on the ground line (y=21)
    real = person_pixels("down", blink=(frame == 2))
    # reflection waves on frames 1-2
    refl = person_pixels("wave" if frame in (1, 2) else "down")
    for sx, sy in real:
        put(px, w, h, sx + 2, sy + 8)
    for sx, sy in refl:
        put(px, w, h, 27 + (13 - sx), sy + 8)
    return img


# ---------------------------------------------------------------------------
# phases.gif — 观象 → 构序 → 观心 → 见性 (four squares light up)
# ---------------------------------------------------------------------------
def draw_phases(frame):
    w, h = 44, 12
    img, px = canvas(w, h)
    squares = [(1, 2), (12, 2), (23, 2), (34, 2)]
    lit = [1, 2, 3, 4, 4, 4, 4, 4][frame]
    for ox, oy in squares[:lit]:
        for x in range(ox, ox + 8):
            for y in range(oy, oy + 8):
                put(px, w, h, x, y)
    return img


# ---------------------------------------------------------------------------
# heart.gif — 心还在跳 (11x8 heart, beat = grows one row)
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
    w, h = 15, 14
    img, px = canvas(w, h)
    rows = HEART + ([".....#....."] if pulse else [])
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                put(px, w, h, x + 2, y + 2)
    return img


# ---------------------------------------------------------------------------
# cursor.gif — terminal block cursor blinking
# ---------------------------------------------------------------------------
def draw_cursor(on):
    w, h = 10, 14
    img, px = canvas(w, h)
    if on:
        for x in range(3, 7):
            for y in range(4, 10):
                put(px, w, h, x, y)
    return img


# ---------------------------------------------------------------------------
# ASCII logo — SE1FAWARE in a custom 5x5 pixel font
# ---------------------------------------------------------------------------
FONT = {
    "S": ["█████", "█....", "█████", "....█", "█████"],
    "E": ["█████", "█....", "████.", "█....", "█████"],
    "1": ["..█..", "..█..", "..█..", "..█..", "█████"],
    "F": ["█████", "█....", "████.", "█....", "█...."],
    "A": ["..█..", ".█.█.", "█████", "█...█", "█...█"],
    "W": ["█...█", "█...█", "█.█.█", "██.██", "█...█"],
    "R": ["████.", "█...█", "████.", "█..█.", "█...█"],
}


def ascii_logo(text="SE1FAWARE"):
    lines = [""] * 5
    for ch in text:
        glyph = FONT[ch]
        for i in range(5):
            lines[i] += glyph[i] + "  "
    return "\n".join(line.rstrip() for line in lines)


def scale(img):
    return img.resize((img.width * SCALE, img.height * SCALE), Image.Resampling.NEAREST)


if __name__ == "__main__":
    # hero: 4 frames x 400ms
    save_gif([scale(draw_hero(i)) for i in range(4)], "hero.gif", 400)
    # phases: fill 1->2->3->4, hold the full state, then snap-reset
    save_gif([scale(draw_phases(i)) for i in range(4)], "phases.gif", [300, 300, 300, 1200])
    # heart: lub-dub, 4 frames x 240ms
    save_gif([scale(draw_heart(p)) for p in (False, True, False, True)], "heart.gif", 240)
    # cursor: 2 frames x 500ms
    save_gif([scale(draw_cursor(True)), scale(draw_cursor(False))], "cursor.gif", 500)

    print()
    print(ascii_logo())
