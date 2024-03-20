# Continuous Valued Game of Life Simulator

Ordinary Conway's game of life is discrete(boolean)-valued cellular automata.

This simulator represents a continuous-valued variant of Conway's game of life.
Each cells has continuous value between 0.0 to 1.0 in this simulator.

## Usage

```
usage: life.py [-h] [--sharpness SHARPNESS] [--fps FPS]
               [--with_grid WITH_GRID] [--loop LOOP] [--movie_file MOVIE_FILE]
               [--movie_duration MOVIE_DURATION] [--gif_file GIF_FILE]
               pattern_file
```

The rule in this simulator can be controlled by single parameter value "sharpness".
Bigger sharpness parameter value mimics discrete-valued cells.
Sharpness parameter value > 5 may represent Conway's Game of Life.

Decreasing the sharpness parameter blunts rule's sigmoidal curve, and obscures the cell's value.

## Files

```
|-- LICENSE
|-- README.md             This file.
|-- life.py               The simulator main codes.
|-- life_display.py       GUI codes.
|-- life_file.py          Life 1.05 pattern file reader/writer.
|-- pattern               Sample Life 1.05 pattern files.
|   |-- acorn.life
|   |-- block.life
|   |-- block3.life
|   |-- block4.life
|   |-- block5.life
|   |-- block6.life
|   |-- glider_gun.life
|   |-- glider_gun1.life
|   |-- glider_ne.life
|   |-- glider_nw.life
|   |-- glider_se.life
|   |-- glider_sw.life
|   |-- puffer_train.life
|   `-- spaceship.life
|-- Makefile              Sample results generator
`-- sample                Sample results
    |-- sharpness1.gif    --sharpness=1 --loop=200
    |-- sharpness2.gif    --sharpness=2 --loop=200
    |-- sharpness3.gif    --sharpness=3 --loop=200
    |-- sharpness4.gif    --sharpness=4 --loop=200
    `-- sharpness5.gif    --sharpness=5 --loop=200
```
