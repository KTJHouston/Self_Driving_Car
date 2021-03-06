from __future__ import annotations
from typing import Tuple, Union
from Vector2D import Vector2D
from shapely.geometry import LineString
from shapely.geometry.point import Point


class Edge:

    def __init__(self, a: Union[Vector2D, Tuple[int, float]], b: Union[Vector2D, Tuple[int, float]]):
        if not isinstance(a, Vector2D):
            a = Vector2D(a[0], a[1])
        if not isinstance(b, Vector2D):
            b = Vector2D(b[0], b[1])
        self.a = a
        self.b = b

    def __copy__(self) -> Edge:
        new_a = self.a.copy()
        new_b = self.b.copy()
        return Edge(new_a, new_b)

    def __eq__(self, other: Edge) -> bool:
        if self.a == other.a:
            if self.b == other.b:
                return True
        elif self.a == other.b:
            if self.b == other.a:
                return True
        return False

    def __getattr__(self, item):
        if item == 'copy':
            return self.__copy__
        return None

    def __getitem__(self, item: int) -> Vector2D:
        if item == 0:
            return self.a
        if item == 1:
            return self.b

    def rotate(self, degrees: Union[int, float]) -> Edge:
        new_a = self.a.rotate(degrees)
        new_b = self.b.rotate(degrees)
        return Edge(new_a, new_b)

    def __setitem__(self, key: int, value: Vector2D) -> None:
        if key == 0:
            self.a = value
        elif key == 1:
            self.b = value
        else:
            raise IndexError

    def shift(self, v: Vector2D) -> Edge:
        new_a = self.a + v
        new_b = self.b + v
        return Edge(new_a, new_b)

    def size(self) -> float:
        return self.a.get_dist(self.b)

    def __str__(self) -> str:
        return "Edge[" + str(self.a) + ", " + str(self.b) + "]"

    def tuple(self):
        return self.a.tuple() + self.b.tuple()

    @staticmethod
    def is_collision(i: Edge, j: Edge) -> bool:
        return Vector2D.is_collision(i.a, i.b, j.a, j.b)

    @staticmethod
    def collision_point(i: Edge, j: Edge) -> Vector2D:
        line1 = LineString([i.a.tuple(), i.b.tuple()])
        line2 = LineString([j.a.tuple(), j.b.tuple()])
        out = line1.intersection(line2)
        if isinstance(out, Point):
            return Vector2D(out.x, out.y)
