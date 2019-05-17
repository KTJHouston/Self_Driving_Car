from unittest import TestCase
from Car import Car
from Wall import Wall
from Vector2D import Vector2D

class TestCar(TestCase):
    def test_adj_pos(self):
        c = Car((10, 20), (128, 128, 255), (10, 10))
        c.adj_pos(Vector2D(20, -10))
        self.assertEqual(c.pos, Vector2D(30, 0))

        c = Car((10, 20), (128, 128, 255), (10, 10))
        c.adj_pos(Vector2D(0, 0))
        self.assertEqual(c.pos, Vector2D(10, 10))

        c = Car((10, 20), (128, 128, 255), (0, 0))
        c.adj_pos(Vector2D(-15, 20))
        self.assertEqual(c.pos, Vector2D(-15, 20))

    def test_adj_dir(self):
        c = Car((10, 20), (128, 128, 255), (0, 0))
        c.adj_dir(.5, 90)
        self.assertAlmostEqual(c.dir, 45)

        c.adj_dir(.01, 90)
        self.assertAlmostEqual(c.dir, 45.9)

        c.adj_dir(.01, 0.15)
        self.assertAlmostEqual(c.dir, 45.9015)

        c.adj_dir(1, -90)
        self.assertAlmostEqual(c.dir, 315.9015)

    def test_collision(self):
        c = Car((10, 20), (128, 128, 255), (0, 0))
        walls = [Wall((-10, -10), (10, 10))]
        self.assertTrue(c.collision(walls))

        walls = [Wall((50, 50), (10, 10))]
        self.assertFalse(c.collision(walls))

        walls = [Wall((100, 100), (50, 50)), Wall((50, 50), (5, 10))]
        self.assertTrue(c.collision(walls))