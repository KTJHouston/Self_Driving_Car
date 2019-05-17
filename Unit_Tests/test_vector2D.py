from unittest import TestCase
from Vector2D import Vector2D


class TestVector2D(TestCase):
    def test___add__(self):
        v1 = Vector2D(2, 3)
        v2 = Vector2D(5, 6)
        a = Vector2D(7, 9)
        self.assertEqual(v1 + v2, a)

        v1 = Vector2D(-2, 3)
        v2 = Vector2D(5, -6)
        a = Vector2D(3, -3)
        self.assertEqual(v1 + v2, a)

    def test___copy__(self):
        v1 = Vector2D(1, 2)
        v2 = v1.copy()
        c = Vector2D(1, 2)
        self.assertEqual(v2, c)

        for i in range(2):
            v1 = Vector2D(1, 2)
            v2 = v1.copy()
            v2[i] = 5
            self.assertNotEqual(v1, v2)

    def test_dot(self):
        v1 = Vector2D(2, 3)
        v2 = Vector2D(5, 6)
        self.assertEqual(v1.dot(v2), 28)

        v1 = Vector2D(2, 3)
        v2 = Vector2D(-3, 2)
        self.assertEqual(v1.dot(v2), 0)

    def test___eq__(self):
        v1 = Vector2D(2, 3)
        v2 = Vector2D(2.0, 3.0)
        self.assertEqual(v1, v2)

        v1 = Vector2D(3, -2)
        v2 = Vector2D(3, -2.0)
        self.assertEqual(v1, v2)

        v1 = Vector2D(3, -2)
        v2 = Vector2D(3, -2.00000001)
        self.assertNotEqual(v1, v2)

        v1 = Vector2D(3, -2)
        v2 = Vector2D(-2, 3)
        self.assertNotEqual(v1, v2)

    def test_find_perp(self):
        v1 = Vector2D(2, 3)
        v2 = v1.find_perp(-3)
        p = Vector2D(-3, 2)
        self.assertEqual(v2, p)

        v1 = Vector2D(2, 3)
        v2 = v1.find_perp(3)
        p = Vector2D(3, -2.0)
        self.assertEqual(v2, p)

        v1 = Vector2D(2, 0)
        v2 = v1.find_perp()
        p = Vector2D(0, 2)
        self.assertEqual(v2, p)

        v1 = Vector2D(0, -1)
        v2 = v1.find_perp()
        p = Vector2D(-1, 0)
        self.assertEqual(v2, p)

    def test_get_dist(self):
        v1 = Vector2D(0.0, -1.0)
        v2 = Vector2D(0.0, 10.0)
        self.assertEqual(v1.get_dist(v2), 11)

        v1 = Vector2D(0, 0)
        v2 = Vector2D(4, 3)
        self.assertEqual(v1.get_dist(v2), 5.0)

        v1 = Vector2D(-2.0, -7)
        v2 = Vector2D(1, -3.0)
        self.assertEqual(v1.get_dist(v2), 5)

    def test_is_perp(self):
        v1 = Vector2D(100, 0)
        v2 = Vector2D(0, 1)
        self.assertTrue(v1.is_perp(v2))

        v1 = Vector2D(100, 0)
        v2 = Vector2D(1, 0)
        self.assertFalse(v1.is_perp(v2))

        v1 = Vector2D(3, 4)
        v2 = Vector2D(3, 4)
        self.assertFalse(v1.is_perp(v2))

        v1 = Vector2D(3, 4)
        v2 = Vector2D(4, -3.0)
        self.assertTrue(v1.is_perp(v2))

    def test___mul__(self):
        v1 = Vector2D(100, 0)
        v2 = Vector2D(0, 1)
        m = Vector2D(0, 0)
        self.assertEqual(v1 * v2, m)

        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        m = Vector2D(3, 8)
        self.assertEqual(v1 * v2, m)

        v1 = Vector2D(.5, -2)
        v2 = Vector2D(3, 4)
        m = Vector2D(1.5, -8)
        self.assertEqual(v1 * v2, m)

    def test___neg__(self):
        v1 = Vector2D(1, 2)
        v2 = -v1
        n = Vector2D(-1, -2)
        self.assertEqual(v2, n)

        v1 = Vector2D(-1, 2)
        v2 = -v1
        n = Vector2D(1, -2)
        self.assertEqual(v2, n)

        v1 = Vector2D(0, 0)
        v2 = -v1
        n = Vector2D(0, 0)
        self.assertEqual(v2, n)

    def test___pow__(self):
        v1 = Vector2D(1, 2)
        v2 = v1 ** 2
        p = Vector2D(1, 4)
        self.assertEqual(v2, p)

        v1 = Vector2D(0, -2)
        v2 = v1 ** 2
        p = Vector2D(0, 4)
        self.assertEqual(v2, p)

        v1 = Vector2D(0, 3)
        v2 = v1 ** 0
        p = Vector2D(1, 1)
        self.assertEqual(v2, p)

        v1 = Vector2D(0, 3)
        v2 = v1 ** 1
        p = Vector2D(0, 3)
        self.assertEqual(v2, p)

    def test_rotate(self):
        v1 = Vector2D(3, 4)
        v2 = v1.rotate(90)
        r = Vector2D(-4, 3.0)
        self.assertAlmostEqualV(v2, r, 4)

        v1 = Vector2D(3, 4)
        v2 = v1.rotate(-90)
        r = Vector2D(4, -3.0)
        self.assertAlmostEqualV(v2, r, 4)

    def test_set_dist(self):
        v1 = Vector2D(3, 4)
        v2 = v1.set_dist(10)
        d = Vector2D(6, 8)
        self.assertEqual(v2, d)

        v1 = Vector2D(-3, -4)
        v2 = v1.set_dist(10)
        d = Vector2D(-6, -8)
        self.assertEqual(v2, d)

        v1 = Vector2D(0, 1)
        v2 = v1.set_dist(10)
        d = Vector2D(0, 10)
        self.assertEqual(v2, d)

        v1 = Vector2D(0, 10)
        v2 = v1.set_dist(1)
        d = Vector2D(0, 1)
        self.assertEqual(v2, d)

    def test___sub__(self):
        v1 = Vector2D(2, 3)
        v2 = Vector2D(5, 6)
        s = Vector2D(-3, -3)
        self.assertEqual(v1 - v2, s)

        v1 = Vector2D(-2, 3)
        v2 = Vector2D(5, -6)
        s = Vector2D(-7, 9)
        self.assertEqual(v1 - v2, s)

        v1 = Vector2D(-2, 3.5)
        v2 = Vector2D(5, -6)
        s = Vector2D(-7, 9.5)
        self.assertEqual(v1 - v2, s)

    def test___truediv__(self):
        v1 = Vector2D(10, 6)
        v2 = Vector2D(5, 2)
        d = Vector2D(2, 3)
        self.assertEqual(v1 / v2, d)

        v1 = Vector2D(11, 6.9)
        v2 = Vector2D(5.5, 3)
        d = Vector2D(2, 2.3)
        self.assertAlmostEqualV(v1 / v2, d)

    def test_tuple(self):
        v = Vector2D(16, 12)
        self.assertEqual(v.tuple(), (16, 12))

        v = Vector2D(16.0, 12)
        self.assertEqual(v.tuple(), (16.0, 12))

    def test_is_collision(self):
        a = Vector2D(0, 0)
        b = Vector2D(5, 5)
        c = Vector2D(5, 0)
        d = Vector2D(0, 5)
        self.assertTrue(Vector2D.is_collision(a, b, c, d))

        a = Vector2D(0, 0)
        b = Vector2D(5, 5)
        c = Vector2D(5, 0)
        d = Vector2D(5, 5)
        self.assertTrue(Vector2D.is_collision(a, b, c, d))

        a = Vector2D(0, 0)
        b = Vector2D(5, 5)
        c = Vector2D(5, 0)
        d = Vector2D(5, 4.99)
        self.assertFalse(Vector2D.is_collision(a, b, c, d))

        a = Vector2D(0, 0)
        b = Vector2D(5, 5)
        c = Vector2D(5, 0)
        d = Vector2D(2.5, 2.5)
        self.assertTrue(Vector2D.is_collision(a, b, c, d))

    def assertAlmostEqualV(self, actual: Vector2D, expected: Vector2D, places: int = 4):
        self.assertAlmostEqual(actual.x, expected.x, places)
        self.assertAlmostEqual(actual.y, expected.y, places)
