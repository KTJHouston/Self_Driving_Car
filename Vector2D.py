from __future__ import annotations
from typing import Union
import math


class Vector2D:

    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.value = (x, y)

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __copy__(self) -> Vector2D:
        return Vector2D(self.x, self.y)

    def dot(self, other: Vector2D) -> Union[int, float]:
        m = self * other
        return m.x + m.y

    def __eq__(self, other: Vector2D) -> bool:
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True

    def find_perp(self, ox: Union[int, float] = 1) -> Vector2D:
        """
        Returns a Vector2D which is perpendicular to the current Vector2D.
        :param ox: Sets the value of the x component of the Vector2D which will be returned. Default 1.
        :return: A Vector2D which is perpendicular, containing the x value given.
        """
        if self.x == 0:
            return Vector2D(self.y, 0)
        elif self.y == 0:
            return Vector2D(0, self.x)
        oy = (-1 * self.x * ox) / self.y
        return Vector2D(ox, oy)

    def __getattr__(self, item):
        if item == 'x':
            return self.value[0]
        elif item == 'y':
            return self.value[1]
        elif item == 'copy':
            return self.__copy__
        return None

    def get_dist(self, other: Vector2D = None) -> float:
        if other is None:
            other = Vector2D(0, 0)
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx ** 2 + dy ** 2) ** .5

    def __getitem__(self, item: int) -> int:
        return self.value[item]

    def is_perp(self, other: Vector2D) -> bool:
        return self.dot(other) == 0

    def __mul__(self, other: Vector2D) -> Vector2D:
        new_x = self.x * other.x
        new_y = self.y * other.y
        return Vector2D(new_x, new_y)

    def __neg__(self) -> Vector2D:
        return Vector2D(-1 * self.x, -1 * self.y)

    def __pow__(self, power, modulo=None) -> Vector2D:
        new_x = self.x.__pow__(power, modulo)
        new_y = self.y.__pow__(power, modulo)
        return Vector2D(new_x, new_y)

    def rotate(self, degrees: Union[int, float]) -> Vector2D:
        rad = math.radians(degrees)
        new_x = math.cos(rad) * self.x - math.sin(rad) * self.y
        new_y = math.sin(rad) * self.x + math.cos(rad) * self.y
        return Vector2D(new_x, new_y)

    def set_dist(self, dist: Union[int, float]) -> Vector2D:
        """
        Returns a Vector2D with the same direction as the current
        Vector2D, but scaled to the magnitude given.
        :param dist: Magnitude of the new Vector2D.
        :return: Vector2D with equal direction and new magnitude.
        """
        d = self.get_dist()
        dt = dist / d
        return self * Vector2D(dt, dt)

    def __setitem__(self, key: int, value: Union[int, float]) -> None:
        if key == 0:
            self.value = (value, self.y)
        elif key == 1:
            self.value = (self.x, value)
        else:
            raise IndexError

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __truediv__(self, other: Vector2D) -> Vector2D:
        new_x = self.x / other.x
        new_y = self.y / other.y
        return Vector2D(new_x, new_y)

    def tuple(self) -> (Union[int, float], Union[int, float]):
        return self.x, self.y

    @staticmethod
    def is_collision(a: Vector2D, b: Vector2D, c: Vector2D, d: Vector2D) -> bool:
        """
        Thank you stack overflow.
        """
        denominator = ((b.x - a.x) * (d.y - c.y)) - ((b.y - a.y) * (d.x - c.x))
        numerator1 = ((a.y - c.y) * (d.x - c.x)) - ((a.x - c.x) * (d.y - c.y))
        numerator2 = ((a.y - c.y) * (b.x - a.x)) - ((a.x - c.x) * (b.y - a.y))

        if denominator == 0:
            return numerator1 == 0 and numerator2 == 0

        r = numerator1 / denominator
        s = numerator2 / denominator

        return 0 <= r <= 1 and 0 <= s <= 1

