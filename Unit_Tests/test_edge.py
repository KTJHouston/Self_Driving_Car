from unittest import TestCase
from Edge import Edge
from Vector2D import Vector2D


class TestEdge(TestCase):
    def test___copy__(self):
        e1 = Edge(Vector2D(1, 2), Vector2D(3, 4))
        e2 = e1.__copy__()
        self.assertEqual(e1, e2)

        e2[0][0] = 5
        self.assertNotEqual(e1, e2)

    def test___eq__(self):
        e1 = Edge(Vector2D(1, 2), Vector2D(3, 4))
        e2 = Edge(Vector2D(1, 2), Vector2D(3, 4))
        self.assertEqual(e1, e2)

        for v in range(2):
            for i in range(2):
                e1 = Edge(Vector2D(1, 2), Vector2D(3, 4))
                e2 = Edge(Vector2D(1, 2), Vector2D(3, 4))
                e1[v][i] = 5
                self.assertNotEqual(e1, e2)

    def test_shift(self):
        e1 = Edge((0, 0), (10, 15))
        v = Vector2D(100, 50)
        e2 = Edge((100, 50), (110, 65))
        self.assertEqual(e1.shift(v), e2)

        e1 = Edge((5, 10), (30, 15))
        v = Vector2D(-20, 40)
        e2 = Edge((-15, 50), (10, 55))
        self.assertEqual(e1.shift(v), e2)

    def test_size(self):
        e1 = Edge(Vector2D(0, 0), Vector2D(3, 4))
        self.assertEqual(e1.size(), 5.0)

        e1 = Edge(Vector2D(15, 10), Vector2D(12, 14))
        self.assertEqual(e1.size(), 5.0)

        e1 = Edge(Vector2D(15, 10), Vector2D(15, 10))
        self.assertEqual(e1.size(), 0.0)

    def test_tuple(self):
        e = Edge((1, 2), (3, 4))
        t = (1, 2, 3, 4)
        self.assertEqual(e.tuple(), t)

        e = Edge(Vector2D(1, 2), (3, 4))
        t = (1, 2, 3, 4)
        self.assertEqual(e.tuple(), t)

        e = Edge((1, 2), Vector2D(3, 4))
        t = (1, 2, 3, 4)
        self.assertEqual(e.tuple(), t)

    def test_is_collision(self):
        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(0, 5))
        self.assertTrue(Edge.is_collision(e1, e2))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(5, 5))
        self.assertTrue(Edge.is_collision(e1, e2))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(5, 5 - 1e-14))
        self.assertFalse(Edge.is_collision(e1, e2))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(2.5, 2.5))
        self.assertTrue(Edge.is_collision(e1, e2))

    def test_collision_point(self):
        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(0, 5))
        self.assertEqual(Edge.collision_point(e1, e2), Vector2D(2.5, 2.5))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(5, 5))
        self.assertEqual(Edge.collision_point(e1, e2), Vector2D(5, 5))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(5, 5 - 1e-14))
        self.assertEqual(Edge.collision_point(e1, e2), None)

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(2.5, 2.5))
        self.assertEqual(Edge.collision_point(e1, e2), Vector2D(2.5, 2.5))
