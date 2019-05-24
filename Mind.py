from typing import List, Tuple
import keras
from keras import layers
import numpy as np
from collections import deque


class Mind:

    def __init__(self, discount_rate: float = .95, learning_rate: float = .001, memory_size: int = 1000):
        self.epsilon = 1.0
        self.discount_rate = discount_rate
        self.adam = keras.optimizers.Adam(learning_rate)
        self.model = None
        self.build_model()
        self.state_mem = deque(maxlen=memory_size)
        self.action_mem = deque(maxlen=memory_size)
        self.reward_mem = deque(maxlen=memory_size)
        self.timer = 0

    def act(self, vision: List[float]) -> Tuple[float, float]:
        """
        The returned floats represent the forward/backward movement and the left/right
        rotation of the car.  For the first float, positive means forward and negative
        means backward.  For the second float, positive means right and negative means
        left.  Both floats will be in the range of (-1, 1)

        :param vision: list of distances to closest walls
        :return: Tuple[float, float]
        """
        state = np.array(vision).reshape(1, 8)
        if np.random.random() < self.epsilon:  # Random action:
            gas = np.random.random()
            if np.random.random() < .5:
                gas *= -1.
            wheel = np.random.random()
            if np.random.random() < .5:
                wheel *= -1.
            output = (gas, wheel)
            action = np.array([gas, wheel]).reshape(1, 2)
        else:  # Best action:
            action = self.model.predict(state)
            output = (action[0, 0], action[0, 1])
        self.state_mem.append(state)
        self.action_mem.append(action)
        return output

    def build_model(self):
        self.model = keras.Sequential()
        self.model.add(layers.InputLayer(batch_input_shape=(1, 8)))
        self.model.add(layers.Dense(16, activation="sigmoid"))
        self.model.add(layers.Dense(8, activation="tanh"))
        self.model.add(layers.Dense(2, activation="tanh"))
        self.model.compile(loss='mse', optimizer=self.adam, metrics=['mae'])

    def reward(self, reward) -> None:
        self.timer += 1
        self.reward_mem.append(reward)
        if reward != 0:  # Apply discount:
            is_punishment = True if reward < 0 else False
            for i in reversed(range(len(self.reward_mem))):
                if i < len(self.reward_mem) - 1:  # If not last element:
                    if self.reward_mem[i] < 0:  # If end of a sequence (crash):
                        break
                    self.reward_mem[i] = self.reward_mem[i] + int(self.discount_rate * self.reward_mem[i + 1])
                if is_punishment:
                    # negate action values:
                    self.action_mem[i] = -1. * self.action_mem[i]

    def train(self):
        self.timer = 0

        # Aliases:
        s = self.state_mem
        a = self.action_mem
        r = self.reward_mem
        for i in range(len(s)):
            if r[i] != 0:
                abs_r = abs(r[i])
                self.model.fit(s[i], a[i], epochs=abs_r, verbose=0)


# m = Mind()
# vision = [5., 2., .5, 1., 5., 3., 2., 4.5]
# p = m.act(vision)
# print(p)
# gas, wheel = m.act(vision)
# print("Gas: {}    Wheel: {}".format(gas, wheel))

'''
def reward(r, new, dr) -> None:
    r.append(new)
    if new != 0:  # Apply discount:
        for i in reversed(range(len(r))):
            if i < len(r) - 1:  # If not last element:
                if r[i] < 0:  # If end of a sequence (crash):
                    break
                r[i] = r[i] + int(dr * r[i + 1])
    return r


f = [0, 0, 0, 0, 0, -5, 0, 0, 0, 100]
dr = .5
r = []
for i in f:
    r = reward(r, i, dr)
    print(r)
'''
