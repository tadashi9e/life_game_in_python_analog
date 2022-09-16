# -*- coding: utf-8; mode:python -*-
import pygame
from typing import Any, List, Mapping, Set, Tuple

class MarginFrame:
    def __init__(self, margin: int = 10) -> None:
        self.x_min = Margin(margin)
        self.y_min = Margin(margin)
        self.x_max = Margin(margin)
        self.y_max = Margin(margin)
    def _set_x_min(self, x: int) -> float:
        return self.x_min.set_min(x)
    def _set_y_min(self, y: int) -> float:
        return self.y_min.set_min(y)
    def _set_x_max(self, x: int) -> float:
        return self.x_max.set_max(x)
    def _set_y_max(self, y: int) -> float:
        return self.y_max.set_max(y)
    def set(self, cells: Set[Tuple[int, int]]) -> Tuple[float, float, float, float]:
        return (
            self._set_x_min(min([x for (x, _) in cells])),
            self._set_y_min(min([y for (_, y) in cells])),
            self._set_x_max(max([x for (x, _) in cells]) + 1),
            self._set_y_max(max([y for (_, y) in cells]) + 1))
class Margin:
    def __init__(self, margin: int):
        self.margin = margin
        self.value = 0.0
    def set_min(self, new_value: int) -> float:
        self.value = (
            new_value - 1 if self.value is None else
            new_value if new_value < self.value else
            (self.value - 0.5) if new_value < self.value + 1 else
            (self.value + 0.25) if new_value > self.value + self.margin else
            self.value)
        return self.value
    def set_max(self, new_value: int) -> float:
        self.value = (
            new_value + 1 if self.value is None else
            new_value if new_value > self.value else
            (self.value + 0.5) if new_value > self.value + 1 else
            (self.value - 0.25) if new_value < self.value - self.margin else
            self.value)
        return self.value
    def get_value(self) -> float:
        return self.value

class LifeDisplay:
    def __init__(self,
                 width: int = 800, height: int = 450,
                 grid_color: Tuple[int, int, int] = (0, 255, 255)) -> None:
        self.MARGIN = 10
        self.width, self.height = width, height
        self.grid_color = grid_color
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.margin_frame = MarginFrame(10)
        pygame.display.set_caption('Life Game')
        self.clock = pygame.time.Clock()
    def clock_tick(self, fps: int) -> None:
        self.clock.tick(fps)
    def _draw_grid(self, cell_size: float,
                   x_center: float,
                   y_center: float,
                   w_center: float,
                   h_center: float) -> None:
        for x in range(int((x_center - w_center / cell_size) / 10) * 10,
                       int(x_center + w_center / cell_size) + 1,
                       10):
            px = int(w_center + (x + 0.5 - x_center) * cell_size)
            pygame.draw.line(self.screen, self.grid_color,
                                 (px, 0), (px, self.height))
        for y in range(int((y_center - h_center / cell_size) / 10) * 10,
                       int(y_center + h_center / cell_size) + 1,
                       10):
            py = int(h_center + (y + 0.5 - y_center) * cell_size)
            pygame.draw.line(self.screen, self.grid_color,
                             (0, py), (self.width, py))
    def color_of(self, value: float) -> Tuple[int, int, int]:
        c = int(255 * (1.0 - value))
        return (c, c, c)
    def draw(self, cells: Mapping[Tuple[int, int], float],
             vaccum_value: float, with_grid: bool = False) -> None:
        x_min, y_min, x_max, y_max = self.margin_frame.set(set(cells.keys()))
        x_cell_size = self.width / (x_max - x_min)
        y_cell_size = self.height / (y_max - y_min)
        cell_size = min(x_cell_size, y_cell_size)
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        w_center = self.width / 2
        h_center = self.height / 2
        self.screen.fill(self.color_of(vaccum_value))
        for (x, y) in cells.keys():
            px = int(w_center + (x - x_center) * cell_size)
            py = int(h_center + (y - y_center) * cell_size)
            px2 = int(w_center + (x + 1 - x_center) * cell_size)
            py2 = int(h_center + (y + 1 - y_center) * cell_size)
            pygame.draw.rect(self.screen, self.color_of(cells[(x, y)]),
                             pygame.Rect(px, py,
                                         px2 - px,
                                         py2 - py))
        if with_grid:
            self._draw_grid(cell_size, x_center, y_center, w_center, h_center)
        pygame.display.flip()
    def generate_animation_gif(self, gen_file_path: str, **kwargs: Any) -> None:
        raise RuntimeError('not implemented')
    def generate_gif(self, gen_file_path: str, **kwargs: Any) -> None:
        raise RuntimeError('not implemented')
        
from PIL import Image
from PIL import ImageDraw

class LifeDisplayAndGenerateImages(LifeDisplay):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(LifeDisplayAndGenerateImages, self).__init__(*args, **kwargs)
        self.images: List[Image] = []
    def draw_grid(self, draw: ImageDraw,
                  cell_size: float, x_center: float, y_center: float,
                  w_center: float, h_center: float) -> None:
        for x in range(int((x_center - w_center / cell_size) / 10) * 10,
                       int(x_center + w_center / cell_size) + 1,
                       10):
            px = int(w_center + (x + 0.5 - x_center) * cell_size)
            draw.line((px, 0, px, self.height), fill=self.grid_color)
        for y in range(int((y_center - h_center / cell_size) / 10) * 10,
                       int(y_center + h_center / cell_size) + 1,
                       10):
            py = int(h_center + (y + 0.5 - y_center) * cell_size)
            draw.line((0, py, self.width, py), fill=self.grid_color)
    def draw(self, cells: Mapping[Tuple[int, int], float],
             vaccum_value: float, with_grid : bool = False) -> None:
        super(LifeDisplayAndGenerateImages, self).draw(
            cells, vaccum_value, with_grid=with_grid)
        image = Image.new('RGB', (self.width, self.height),
                          self.color_of(vaccum_value))
        draw = ImageDraw.Draw(image)
        x_min, y_min, x_max, y_max = self.margin_frame.set(set(cells.keys()))
        x_cell_size = self.width / (x_max - x_min)
        y_cell_size = self.height / (y_max - y_min)
        cell_size = min(x_cell_size, y_cell_size)
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        w_center = self.width / 2
        h_center = self.height / 2
        self.screen.fill(self.color_of(vaccum_value))
        for (x, y) in cells.keys():
            px = int(w_center + (x - x_center) * cell_size)
            py = int(h_center + (y - y_center) * cell_size)
            px2 = int(w_center + (x + 1 - x_center) * cell_size)
            py2 = int(h_center + (y + 1 - y_center) * cell_size)
            draw.rectangle((px, py, px2, py2),
                           fill=self.color_of(cells[(x, y)]))
        if with_grid:
            self.draw_grid(draw, cell_size, x_center, y_center, w_center, h_center)
        self.images.append(image)
    def generate_animation_gif(self, gen_file_path: str, **kwargs: Any) -> None:
        self.images[0].save(gen_file_path,
                            save_all=True, append_images=self.images[1:],
                            **kwargs)
    def generate_gif(self, gen_file_path: str, **kwargs: Any) -> None:
        self.images[-1].save(gen_file_path,
                             save_all=True,
                             **kwargs)
