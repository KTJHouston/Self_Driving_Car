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

    def test_size(self):
        e1 = Edge(Vector2D(0, 0), Vector2D(3, 4))
        self.assertEqual(e1.size(), 5.0)

        e1 = Edge(Vector2D(15, 10), Vector2D(12, 14))
        self.assertEqual(e1.size(), 5.0)

        e1 = Edge(Vector2D(15, 10), Vector2D(15, 10))
        self.assertEqual(e1.size(), 0.0)

    def test_is_collision(self):
        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(0, 5))
        self.assertTrue(Edge.is_collision(e1, e2))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(5, 5))
        self.assertTrue(Edge.is_collision(e1, e2))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(5, 4.99))
        self.assertFalse(Edge.is_collision(e1, e2))

        e1 = Edge(Vector2D(0, 0), Vector2D(5, 5))
        e2 = Edge(Vector2D(5, 0), Vector2D(2.5, 2.5))
        self.assertTrue(Edge.is_collision(e1, e2))
