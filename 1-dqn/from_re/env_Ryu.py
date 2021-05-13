from math import *
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np


def euclidean_distance(pt1, pt2):
    distance = 0
    for i in range(len(pt1)):
        distance += (pt1[i] - pt2[i]) ** 2
    return distance ** 0.5


class VrpEnv(object):
    def __init__(self, x, y, cap):
        self.customer_x = x
        self.customer_y = y
        self.capacity = cap
        self.node_size = 10
        self.depot_x = 40
        self.depot_y = 50
        self.speed = 70

        self.max_x = 100
        self.max_y = 100
        self.threshold_capacity = 20
        self.threshold_time = 60 * 24

        self.action_space = spaces.Discrete(self.node_size)
        high = np.array([self.max_x, np.finfo(np.float32).max,
                                             self.max_y,
                                             np.finfo(np.float32).max],
                                            dtype=np.float32)
        self.observation_space = spaces.Box(-high,high,
                                            dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        x, y, capacity, time = self.state
        next_x = self.customer_x[action]
        next_y = self.customer_y[action]
        #self.node_check[action] = False

        next_time = time + (euclidean_distance((x, y), (next_x, next_y)) / self.speed)

        capacity -= self.capacity[action]

        self.state = (next_x, next_y, capacity, next_time)

        done = bool(
            capacity == 0
            or x < -self.max_x
            or x > self.max_x
            or y < -self.max_y
            or y > self.max_y
        )

        if not done:
            reward = 0.1
        elif self.steps_beyond_done is None:
            self.steps_beyond_done = 0
            reward = 0.1
        else:
            if self.steps_beyond_done == 0:
                logger.warn(
                    "You are calling 'step()' even though this "
                    "environment has already returned done = True. You "
                    "should always call 'reset()' once you receive 'done = "
                    "True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = (40, 50, 10, 0)
        self.steps_beyond_done = None
        return np.array(self.state)
