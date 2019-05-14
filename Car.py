from typing import List, Tuple
import pyglet as pg
from pyglet.window import key
from Vector2D import Vector2D
from Wall import Wall


class Car:

    def __init__(self, size: (int, int), color: (int, int, int), start: (int, int) = (0, 0), dir: int = 0):
        """
        Initialization.
        :param size: (width, height)
        :param color: (R, G, B)
        :param start: (X, Y) coordinate
        :param dir: int degree of rotation modulo 360
        """
        self.pos = Vector2D(start[0], start[1])
        self.size = Vector2D(size[0], size[1])
        self.rel_corners = []
        for i in range(4):
            self.rel_corners.append(self.get_relative_corner(i))
        self.dir = dir % 360
        self.set_color(color)
        self.color = (0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0)  # TODO Remove for color normal setting
        self.speed = 4
        self.is_dead = False

    def adj_pos(self, adj: Vector2D) -> None:
        self.pos = self.pos + adj

    def adj_dir(self, adj: int) -> None:
        self.dir = (self.dir + adj) % 360

    def collision(self, walls: List[Wall]) -> bool:
        edges = self.get_edges()
        for w in walls:
            for e in edges:
                input = e + w.as_edge()
                if Vector2D.is_collision(*input):
                    return True
        return False

    def draw(self) -> None:
        pg.graphics.draw(4, pg.gl.GL_QUADS,
                         ('v2f', self.get_verts()),
                         ('c3B', self.color))

    def get_edges(self) -> List[Tuple[Vector2D, Vector2D]]:
        relative = []
        # Rotate relative corners:
        for i in range(4):
            vec = self.rel_corners[i]
            rot = vec.rotate(self.dir)
            relative.append(rot)

        # Displace relative corners by pos:
        verts = []
        for i in range(4):
            verts.append(self.pos + relative[i])

        # Combine pairs of vertices for edges
        edges = []
        for i in range(4):
            e = (verts[i], verts[(i+1) % 4])
            edges.append(e)
        return edges

    def get_relative_corner(self, num):
        if num == 0:
            d = Vector2D(2, 2)
        elif num == 1:
            d = Vector2D(2, -2)
        elif num == 2:
            d = Vector2D(-2, -2)
        elif num == 3:
            d = Vector2D(-2, 2)
        else:
            raise IndexError
        return self.size / d

    def get_verts(self):
        relative = []
        # Rotate relative corners:
        for i in range(4):
            vec = self.rel_corners[i]
            rot = vec.rotate(self.dir)
            relative.append(rot)

        # Displace relative corners by pos:
        output = ()
        for i in range(4):
            new = self.pos + relative[i]
            output = output + new.tuple()
        return output

    def move_forward(self, dist):
        forward = Vector2D(0, dist)
        rot = forward.rotate(self.dir)
        self.adj_pos(rot)

    def set_color(self, color) -> None:
        self.color = ()
        for i in range(4):
            self.color += color

    def update(self, dt, keys_pressed, last_keys, walls) -> None:
        if self.is_dead:
            return
        if keys_pressed[key.W]:
            self.move_forward(self.speed)
        if keys_pressed[key.S]:
            self.move_forward(-self.speed)
        if keys_pressed[key.D]:
            self.adj_dir(-3)
        if keys_pressed[key.A]:
            self.adj_dir(3)
        if self.collision(walls):
            self.set_color((221, 22, 22))
            self.is_dead = True
        else:
            self.color = (0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0)

