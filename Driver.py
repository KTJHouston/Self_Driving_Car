from typing import List, Dict
import pyglet as pg
from Car import Car
from Mind import Mind
from Wall import Wall
from RewardGate import RewardGate
from Edge import Edge


class Driver:

    def __init__(self, car: Car, show_vision: bool = False):
        self.car = car
        self.original_car = car.__copy__()
        self.mind = Mind()
        self.show_vision = show_vision
        self.vision = []  # List[Edge]
        self.collisions = []  # List[Vector2D]
        self.counter = 0
        self.buffer = 5

    def check_rewards(self, rgs: List[RewardGate]) -> int:
        edges = self.car.get_edges()
        for i in range(len(rgs)):
            for e in edges:
                if Edge.is_collision(e, rgs[i].as_edge()):
                    reward = RewardGate.trigger(i, rgs)
                    if reward > 0:
                        return reward
        return 0

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

    def update(self, dt: float, walls: List[Wall], rgs: List[RewardGate]) -> bool:
        if self.buffer > 0:
            self.buffer -= 1
            return False
        self.counter += 1
        vision = self.find_state(walls)
        gas, wheel = self.mind.act(vision)
        gas *= 200
        wheel *= 150
        done = self.car.update_nn(dt, gas, wheel, walls)
        r = 0
        if done:
            r += -5
        r += self.check_rewards(rgs) * 20
        self.mind.reward(r)
        if done:
            self.mind.train()
            if self.mind.epsilon > .05:
                self.mind.epsilon = self.mind.epsilon * .95
            else:
                self.mind.epsilon = .05
            self.set_car(self.original_car.__copy__())
            print("Counter: {} Eps: {}".format(self.counter, self.mind.epsilon))
            print("Rewards: ", self.mind.reward_mem)
            self.counter = 0
            self.buffer = 5
            return True
        return False
