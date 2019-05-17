from unittest import TestCase
from Wall import Wall
from Edge import Edge
from Vector2D import Vector2D


class TestWall(TestCase):
    def test_as_edge(self):
        w = Wall((0, 0), (15, 10))
        e = Edge(Vector2D(0, 0), Vector2D(15, 10))
        self.assertEqual(w.as_edge(), e)

        w = Wall((0, 0), (15, 10))
        e = Edge(Vector2D(15, 10), Vector2D(0, 0))
        self.assertEqual(w.as_edge(), e)

    def test_get_corner(self):
        w = Wall((0, 0), (0, 10), 4)
        vecs = [Vector2D(2, 0), Vector2D(-2, 0), Vector2D(-2, 10), Vector2D(2, 10)]
        for i in range(4):
            self.assertEqual(w.get_corner(i), vecs[i])

    def test_get_verts(self):
        w = Wall((0, 0), (0, 10), 4)
        v = (2, 0, -2, 0, -2, 10, 2, 10)
        self.assertEqual(w.get_verts(), v)
