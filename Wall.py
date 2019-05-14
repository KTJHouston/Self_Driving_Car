from typing import Tuple
import pyglet as pg
from Vector2D import Vector2D


class Wall:

    def __init__(self, a: (int, int), b: (int, int), width: int = 4):
        self.a = Vector2D(a[0], a[1])
        self.b = Vector2D(b[0], b[1])
        self.width = width
        color = (155, 155, 155)
        self.color = ()
        for i in range(4):
            self.color += color

    def as_edge(self) -> (Vector2D, Vector2D):
        return self.a, self.b

    def draw(self) -> None:
        pg.graphics.draw(4, pg.gl.GL_QUADS,
                         ('v2f', self.get_verts()),
                         ('c3B', self.color))

    def get_corner(self, num: int) -> Vector2D:
        diff = self.b - self.a
        perp = diff.find_perp()
        perp = perp.set_dist(self.width // 2)
        if num == 0:
            return self.a + perp
        elif num == 1:
            return self.a + -perp
        elif num == 2:
            return self.b + -perp
        elif num == 3:
            return self.b + perp

    def get_verts(self) -> Tuple[int]:
        output = ()
        for i in range(4):
            output = output + self.get_corner(i).tuple()
        return output

    def __str__(self) -> str:
        return "Wall(" + str(self.a) + ", " + str(self.b) + ")"

    def update(self, dt: float) -> None:
        pass

