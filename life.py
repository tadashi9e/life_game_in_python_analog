# -*- coding: utf-8; mode:python -*-
import argparse
import life_file
import cupy as xp
from cupyx.scipy import signal
import cv2

class Field(object):
    def __init__(self, width: int, height: int, sharpness: float):
        self._width = width
        self._height = height
        # Cells
        self._cells = xp.zeros((height, width), dtype = xp.float32)
        # Sharpness paraneter
        self._sharpness = sharpness
        # Moore neighborhood
        self._neighbours = xp.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]], dtype = xp.float16)
    def init_random(self):
        u'''
        Initialize all cells with random value.
        '''
        self._cells = xp.random.rand(self._height, self._width,
                                     dtype = xp.float32)
    def mask(self) -> None:
        u'''
        Clear field except center.
        '''
        mesh_y, mesh_x = xp.meshgrid(
            xp.arange(self._height),
            xp.arange(self._width))
        self._cells[xp.where(mesh_y < self._height / 3)] = 0
        self._cells[xp.where(mesh_y > self._height * 2 / 3)] = 0
        self._cells[xp.where(mesh_x < self._width / 3)] = 0
        self._cells[xp.where(mesh_x > self._width * 2 / 3)] = 0

    def read_life_105_file(self, x: int, y: int, path: str):
        u'''
        Read Life1.05 format file.
        '''
        dots = life_file.read_life_105_file(x, y, path)
        life_file.write_life_105(dots)
        for (x, y) in dots:
            self._cells[y % self._height][x % self._width] = 1.0
    def get_current_cells(self):
        u'''
        Get current field image.
        '''
        v = (self._cells * 255).astype(xp.uint8)
        img = xp.stack([v, v, v], axis = 2)
        return xp.asnumpy(img)
    def update_cells(self) -> None:
        u'''
        Update cells.
        '''
        n_sum = signal.convolve2d(self._cells, self._neighbours,
                                  mode = 'same', boundary = 'wrap')
        self._cells = 0.5 * (
            xp.tanh(self._sharpness * (n_sum - (2.5 - self._cells))) *
            xp.tanh(self._sharpness * (3.5 - n_sum)) + 1.0)

def main() -> None:
    # --- Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type = int, default = 200,
                        help = 'Field width')
    parser.add_argument('--sharpness', type = float, default = 5.0,
                        help = 'Sharpness parameter')
    parser.add_argument('--height', type = int, default = 200,
                        help = 'Field height')
    parser.add_argument('--pattern', type = str, default = None,
                        help = 'Initial pattern file')
    args = parser.parse_args()
    width = int(args.width)
    height = int(args.height)
    sharpness = args.sharpness
    pattern_file = args.pattern
    waiting = 10
    # --- Calculate and display loop
    field = Field(width, height, sharpness)
    if pattern_file:
        field.read_life_105_file(
            int(width / 2), int(height / 2), pattern_file)
    else:
        field.init_random()
        field.mask()
    while True:
        field.update_cells()
        cells = field.get_current_cells()
        cv2.imshow("Game of Life", cells)
        r = cv2.waitKey(waiting)
        if r == ord("+"):
            waiting = max(10, waiting//2)
        if r == ord("-"):
            waiting = min(1000, waiting*2)
        if r == ord("q"):
            break

if __name__ == '__main__':
    main()
