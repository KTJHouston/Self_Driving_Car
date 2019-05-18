from typing import List, Tuple, Union, Dict
import pyglet as pg
from pyglet.window import key
from Vector2D import Vector2D
from Wall import Wall
from Edge import Edge


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
        self.speed = 200
        self.turning_rate = 135
        self.is_dead = False

    def adj_pos(self, adj: Vector2D) -> None:
        self.pos = self.pos + adj

    def adj_dir(self, dt: float, turning_rate: Union[int, float]) -> None:
        adj = dt * turning_rate
        self.dir = (self.dir + adj) % 360

    def collision(self, walls: List[Wall]) -> bool:
        edges = self.get_edges()
        for w in walls:
            for e in edges:
                if Edge.is_collision(e, w.as_edge()):
                    return True
        return False

    def draw(self) -> None:
        pg.graphics.draw(4, pg.gl.GL_QUADS,
                         ('v2f', self.get_verts()),
                         ('c3B', self.color))

    def get_edges(self) -> List[Edge]:
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
            e = Edge(verts[i], verts[(i+1) % 4])
            edges.append(e)
        return edges

    def get_relative_corner(self, num: int) -> Vector2D:
        """
        This SHOULD only need to be computed once, at initialization.
        OR whenever size changes. These vertices aid in the computation
        of the dynamic edges and verts.
        :param num:
        :return:
        """
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

    def get_verts(self) -> Tuple[int, float]:
        """
        Returns a tuple or ints or floats corresponding to
        where each vertex of the Car should be drawn.
        :return:
        """
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

    def move_forward(self, dt: float, speed: Union[int, float]) -> None:
        dist = dt * speed
        forward = Vector2D(0, dist)
        rot = forward.rotate(self.dir)
        self.adj_pos(rot)

    def set_color(self, color: (int, int, int)) -> None:
        self.color = ()
        for i in range(4):
            self.color += color

    def update(self, dt: float, keys_pressed: Dict[int, bool], walls: List[Wall]) -> None:
        if self.is_dead:
            return
        if keys_pressed[key.W]:
            self.move_forward(dt, self.speed)
        if keys_pressed[key.S]:
            self.move_forward(dt, -self.speed)
        if keys_pressed[key.D]:
            self.adj_dir(dt, -self.turning_rate)
        if keys_pressed[key.A]:
            self.adj_dir(dt, self.turning_rate)
        if self.collision(walls):
            self.set_color((221, 22, 22))
            self.is_dead = True

