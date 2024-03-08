import argparse

import numpy as np
import pygame as pg
from pygame import gfxdraw as gfx


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--fg",
        type=str,
        help="Foreground color of the curve in hex format (eg. ff0000)",
        default="ff0000",
    )
    parser.add_argument(
        "-b",
        "--bg",
        type=str,
        help="Background color in hex format (eg. 000000)",
        default="000000",
    )
    parser.add_argument(
        "-t",
        "--thickness",
        type=int,
        help="Line thickness in pixels (eg. 10)",
        default=10,
    )
    parser.add_argument(
        "-s",
        "--speed",
        type=int,
        help="Speed (eg. 15)",
        default=60,
    )
    parser.add_argument(
        "-V",
        "--vertical",
        type=int,
        help="Vertical frequency (eg. 5)",
        default=5,
    )
    parser.add_argument(
        "-H",
        "--horizontal",
        type=int,
        help="Horizontal frequency (eg. 4)",
        default=4,
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Window height (eg. 800)",
        default=800,
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Window width (eg. 800)",
        default=800,
    )
    parser.add_argument(
        "--npoints",
        type=int,
        help="Number of domain points - resolution (eg. 5000)",
        default=5000,
    )

    return parser.parse_args()


def lissajous(v, h, n, width, height):
    period = 2 * np.pi / np.gcd(h, v)
    time = np.linspace(0, period, n)

    return np.array(
        [
            np.sin(time * v) * width / 3 + width / 2,
            np.sin(time * h) * height / 3 + height / 2,
        ]
    ).T.astype("int")


def draw_lissjous(surface, points, length, shift, thickness, color):
    for i in range(length):
        n = (i + shift) % length
        color.a = int(255 * i / length)
        gfx.filled_circle(surface, points[n][0], points[n][1], thickness, color)


def animate():
    args = get_args()
    args.bg = "#" + args.bg
    args.fg = "#" + args.fg

    pg.init()
    pg.display.set_caption("Lissajous curve")

    clock = pg.time.Clock()

    screen = pg.display.set_mode((args.width, args.height))
    screen.fill(pg.Color(args.bg))
    s = pg.Surface((args.width, args.height), pg.SRCALPHA)

    points = lissajous(
        args.vertical, args.horizontal, args.npoints, args.width, args.height
    )
    shift = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        screen.fill(pg.Color(args.bg))
        s.fill((0, 0, 0, 0))

        draw_lissjous(s, points, args.npoints, shift, args.thickness, pg.Color(args.fg))

        shift = (shift + args.speed) % args.npoints

        screen.blit(s, (0, 0))
        pg.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    animate()
