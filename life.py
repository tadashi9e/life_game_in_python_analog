# -*- coding: utf-8; mode:python -*-
import argparse
import math
import os
import sys
import collections
import life_display
import life_file
from typing import Dict, Tuple

def sig(x: float) -> float:
    u'''Sigmoid function
    '''
    return math.tanh(x)
def rect(sharpness: float, a: float, b: float, x: float) -> float:
    u'''Rectangular function.

    Arguments
    --------
    sharpness: Approximation parameter
    a: Rectangle lower limit
    b: Rectangle higher limit
    x: Target value

    Returns
    --------
    Positive value when a < x < b, otherwise returns negative.
    '''
    return 0.5 * (sig(sharpness * (x - a)) * sig(sharpness * (b - x)) + 1)
def sum_neighbours(cells: Dict[Tuple[int, int], float],
                   point: Tuple[int, int],
                   vaccum_value: float) -> float:
    u'''Get sum of neighbor cell values.

    Arguments
    --------
    cells: All cells.
    point: Target cell position.

    Returns
    --------
    Sum of neighbor cell values.
    '''
    (px, py) = point
    return sum([cells.get(pd, vaccum_value)
                for pd in [(px + dx, py + dy)
                           for dx in range(-1, 2)
                           for dy in range(-1, 2)
                           if dx != 0 or dy != 0]])
def next_cell_value(cells: Dict[Tuple[int, int], float],
                    sharpness: float,
                    point: Tuple[int, int],
                    vaccum_value: float) -> float:
    u'''Get next value of cell at a point

    Arguments
    --------
    cells: Current cells.
    sharpness: Approximation parameter of rectangular function.
    point: Target cell position.

    Returns
    --------
    Next value of target cell.
    '''
    sum = sum_neighbours(cells, point, vaccum_value)
    a = 2.5 - cells.get(point, vaccum_value)
    b = 3.5
    return rect(sharpness, a, b, sum)

def estimate_vaccum_value(sharpness: float, loop: int = 100) -> float:
    u'''Estimate vaccum value of cell space.

    Arguments
    --------
    sharpness: Approximation parameter of rectangular function.
    loop: Loop count for estimation.

    Returns
    --------
    Estimated vaccume value of cell space.
    '''
    v = 0.0
    for i in range(loop):
        a = 2.5 - v
        b = 3.5
        v = rect(sharpness, a, b, 8 * v)
    return v

def life(cells: Dict[Tuple[int, int], float],
         sharpness: float,
         vaccum_value: float,
         epsilon: float) -> Dict[Tuple[int, int], float]:
    u'''Get next cells.

    Arguments
    --------
    cells: Current cells.
    sharpness: Approximation parameter of rectangular function.
    vaccum_value: Vaccume value of cell space.
    epsilon: small value.

    Returns
    --------
    Next step cells.
    '''
    return dict([
        (p, v)
        for (p, v) in [
                (point, next_cell_value(cells, sharpness, point, vaccum_value))
                for point in set([(px + dx, py + dy)
                                  for (px, py) in cells.keys()
                                  for dx in range(-1, 2)
                                  for dy in range(-1, 2)])]
        if (v > vaccum_value + epsilon or
            v < vaccum_value - epsilon)])

EPSILON = 0.000001

def main() -> None:
    # --- Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern_file')
    parser.add_argument('--sharpness', type = float, default = 5,
                        help = 'Sharpness parameter')
    parser.add_argument('--fps', type = int, default = 10,
                        help = 'Simulation frame rate')
    parser.add_argument('--with_grid', type = bool, default = False,
                        help = 'Draw image with grid')
    parser.add_argument('--loop', type = int, default = 0,
                        help = 'Maximum loop count')
    parser.add_argument('--movie_file', default = '',
                        help = 'GIF movie output file path')
    parser.add_argument('--movie_duration', type = int, default = 1000,
                        help = 'GIF movie duration')
    parser.add_argument('--gif_file', default = '',
                        help = 'GIF output file path')
    args = parser.parse_args()
    sharpness = float(args.sharpness)
    fps = int(args.fps)
    with_grid = args.with_grid
    loop = int(args.loop)
    movie_duration = int(args.movie_duration)
    if args.movie_file and loop == 0:
        print('--movie_file requires --loop')
        sys.exit(1)
    if args.gif_file and loop == 0:
        print('--gif_file requires --loop')
        sys.exit(1)
    # --- Load initial cells from Life1.05 file
    dots = life_file.read_life_105_file(0, 0, args.pattern_file)
    cells = dict([((x, y), 1.0) for (x, y) in dots])
    vaccum_value = estimate_vaccum_value(sharpness)
    print('vaccum={}'.format(vaccum_value))
    # --- Calculate and display loop
    display = (
        life_display.LifeDisplayAndGenerateImages(width=200, height=200)
        if args.movie_file or args.gif_file else
        life_display.LifeDisplay())
    i = 0
    while True:
        if loop != 0 and i >= loop:
            break
        i += 1
        display.draw(cells, vaccum_value, with_grid = with_grid)
        cells = life(cells, sharpness, vaccum_value, EPSILON)
        if not cells:
            print('all cells vanished')
            break
        display.clock_tick(fps)
    # --- Generate GIF file if required
    if args.movie_file:
        display.generate_animation_gif(args.movie_file,
                                       optimize=True,
                                       duration=movie_duration, loop=0)
    if args.gif_file:
        display.generate_gif(args.gif_file,
                             optimize=True)

if __name__ == '__main__':
    main()
