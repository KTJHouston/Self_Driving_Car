from typing import List, Dict
import pyglet as pg
from Car import Car
from Wall import Wall
from Edge import Edge


class Driver:

    def __init__(self, car: Car, show_vision: bool = False):
        # TODO pass driver a neural net controller
        self.car = car
        self.show_vision = show_vision
        self.vision = []  # List[Edge]
        self.collisions = []  # List[Vector2D]

    def draw(self) -> None:
        self.car.draw()
        if self.show_vision:
            for v in self.vision:
                # Draw vision lines
                pg.graphics.draw(2, pg.gl.GL_LINES,
                                 ('v2f', v.tuple()))
            for cp in self.collisions:
                # Draw collision points
                pg.graphics.draw(1, pg.gl.GL_POINTS,
                                 ('v2f', cp.tuple()),
                                 ('c3B', (66, 134, 244)))

    def find_state(self, walls: List[Wall]) -> List[float]:
        """
        Calculates the distances to the nearest wall in eight directions.
        Returns the distances as a list. Index 0 going straight ahead,
        and then each rotating clockwise 45 degrees.
        :param walls: List of Wall objects which can be "seen."
        :return: List of floats which are the distances to wall objects in various directions.
        """

        out = []
        self.vision = []
        self.collisions = []

        view_distance = 125
        base_edge = Edge((0, 0), (0, view_distance))
        for i in range(8):
            sight_line = base_edge.copy()
            degrees = self.car.dir + 45 * i
            sight_line.b = sight_line.b.rotate(degrees)
            sight_line = sight_line.shift(self.car.pos)
            self.vision.append(sight_line)

        for v in self.vision:  # For each line of sight
            shortest = view_distance
            for w in walls:  # For each wall
                tmp = Edge.collision_point(v, w.as_edge())
                if tmp is not None:  # If driver can see something:
                    # Append location:
                    self.collisions.append(tmp)
                    # Calculate distance:
                    edge_tmp = Edge(v.a, tmp)
                    size_tmp = edge_tmp.size()
                    if size_tmp < shortest:
                        # Compare to shortest found so far:
                        shortest = size_tmp
            # Append shortest distance seen:
            out.append(shortest)
        return out

    def set_car(self, car: Car) -> None:
        self.car = car

    def update(self, dt: float, keys_pressed: Dict[int, bool], walls: List[Wall]) -> None:
        vision = self.find_state(walls)
        # TODO pass state to NN to find actions
        # TODO pass actions to car
        self.car.update(dt, keys_pressed, walls)
