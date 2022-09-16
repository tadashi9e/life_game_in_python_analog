# -*- coding: utf-8; mode:python -*-
import sys
from typing import TextIO, Set, Tuple

def _parse_line(line: str, x0: int, y: int) -> Set[Tuple[int, int]]:
    return {(x0 + i, y) for i in range(len(line)) if line[i] == '*'}

def read_life_105(x0: int, y0: int, stream: TextIO) -> Set[Tuple[int, int]]:
    dots: Set[Tuple[int, int]] = set()
    y = y0
    for line in stream:
        if line.startswith('#'):
            continue
        if not line.rstrip('\r\n'):
            continue
        dots |= _parse_line(line, x0, y)
        y += 1
    return dots
def write_life_105(dots: Set[Tuple[int, int]],
                   stream: TextIO = sys.stdout) -> None:
    x_min = min([x for (x, _) in dots])
    y_min = min([y for (_, y) in dots])
    x_max = max([x for (x, _) in dots])
    y_max = max([y for (_, y) in dots])
    print('#P {} {}'.format(x_min, y_min))
    for y in range(y_min, y_max + 1):
        line = ''.join([('*' if (x, y) in dots else '.')
                        for x in range(x_min, x_max + 1)])
        stream.write(line + '\n')
def read_life_105_file(x0: int, y0: int, from_path: str) -> Set[Tuple[int, int]]:
    with open(from_path, 'r') as f:
        return read_life_105(x0, y0, f)

def write_life_105_file(dots: Set[Tuple[int, int]], to_path: str) -> None:
    with open(to_path, 'w', newline='\r\n') as f:
        f.write('#Life 1.05\n')
        write_life_105(dots, f)
