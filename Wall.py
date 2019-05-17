from typing import Tuple
import pyglet as pg
from Edge import Edge
from Vector2D import Vector2D


class Wall:

    def __init__(self, a: (int, int), b: (int, int), width: int = 4):
        a = Vector2D(a[0], a[1])
        b = Vector2D(b[0], b[1])
        self.e = Edge(a, b)
        self.width = width
        color = (155, 155, 155)
        self.color = ()
        for i in range(4):
            self.color += color

    def as_edge(self) -> Edge:
        return self.e

    def draw(self) -> None:
        pg.graphics.draw(4, pg.gl.GL_QUADS,
                         ('v2f', self.get_verts()),
                         ('c3B', self.color))

    def get_corner(self, num: int) -> Vector2D:
        diff = self.e.b - self.e.a
        perp = diff.find_perp()
        perp = perp.set_dist(self.width // 2)
        if num == 0:
            return self.e.a + perp
        elif num == 1:
            return self.e.a + -perp
        elif num == 2:
            return self.e.b + -perp
        elif num == 3:
            return self.e.b + perp

    def get_verts(self) -> Tuple[int]:
        # TODO call only once at the beginning
        output = ()
        for i in range(4):
            output = output + self.get_corner(i).tuple()
        return output

    def __str__(self) -> str:
        return "Wall(" + str(self.a) + ", " + str(self.e.b) + ")"

    def update(self, dt: float) -> None:
        pass

