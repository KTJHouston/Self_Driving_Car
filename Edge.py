from __future__ import annotations
from Vector2D import Vector2D


class Edge:

    def __init__(self, a: Vector2D, b: Vector2D):
        self.a = a
        self.b = b

    def __copy__(self) -> Vector2D:
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
        return None

    def __setitem__(self, key: int, value: Vector2D) -> None:
        if key == 0:
            self.a = value
        elif key == 1:
            self.b = value
        else:
            raise IndexError

    def size(self) -> float:
        return self.a.get_dist(self.b)

    def __str__(self) -> str:
        return "Edge[" + str(self.a) + ", " + str(self.b) + "]"

    @staticmethod
    def is_collision(i: Edge, j: Edge) -> bool:
        return Vector2D.is_collision(i.a, i.b, j.a, j.b)
