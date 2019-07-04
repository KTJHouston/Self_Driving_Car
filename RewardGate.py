from __future__ import annotations
from typing import List, Tuple
import pyglet as pg
from Edge import Edge
from Vector2D import Vector2D


class RewardGate:

    def __init__(self, a: (int, int), b: (int, int), is_on: bool = True, show: bool = True, width: int = 4):
        self.e = Edge(a, b)
        self.width = width
        self.verts = self.get_verts()
        self.show = show  # Whether it should be displayed
        self.is_on = is_on  # If it can be trigger by driver for a reward

        self.blue = (66, 80, 244)
        self.red = (221, 22, 22)
        self.color = ()
        self.flip(is_on)

    def as_edge(self) -> Edge:
        return self.e

    def draw(self) -> None:
        if self.show:
            pg.graphics.draw(4, pg.gl.GL_QUADS,
                             ('v2f', self.verts),
                             ('c3B', self.color))

    def __getattr__(self, item):
        if item == 'a':
            return self.e.a
        elif item == 'b':
            return self.e.b
        return None

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
        output = ()
        for i in range(4):
            output = output + self.get_corner(i).tuple()
        return output

    def set_color(self, color: Tuple[int, int, int]) -> None:
        self.color = ()
        for i in range(4):
            self.color += color

    def __str__(self) -> str:
        return "RewardGate(" + str(self.e.a) + ", " + str(self.e.b) + ")"

    def update(self, dt: float) -> None:
        pass

    def flip(self, is_on: bool) -> None:
        self.is_on = is_on
        if is_on:
            self.set_color(self.blue)
        else:
            self.set_color(self.red)

    @staticmethod
    def trigger(index: int, gates: List[RewardGate]) -> int:
        space = 5
        if gates[index].is_on:
            gates[index].flip(False)
            to_turn_on = (index - space) % len(gates)
            gates[to_turn_on].flip(True)
            return 1
        else:
            to_turn_on = (index - space) % len(gates)
            gates[to_turn_on].flip(True)
        return 0
