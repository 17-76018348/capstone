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
    def __init__(self, nodes):
        self.customer_x = nodes['map_coored'][0]
        self.customer_y = nodes['map_coored'][1]
        self.capacity = nodes['capacity']
        self.node_size = len(nodes)
        self.depot_x = 40
        self.depot_y = 50
        self.speed = 70
        self.node_check = [True for _ in range(self.node_size)]

        self.threshold_capacity = 20
        self.threshold_time = 60 * 24

        self.action_space = spaces.Discrete(len(self.node_size))
        self.opservation_space = spaces.Box()

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action, reward):
        x, y, capacity, time, complete_requests = self.state
        next_x = self.customer_x[action]
        next_y = self.customer_y[action]
        self.node_check[action] = False

        next_time = time + (euclidean_distance((x, y), (next_x, next_y)) / self.speed)

        capacity -= self.capacity[action]

        self.state = (next_x, next_y, capacity, next_time)

        done = bool(
            capacity > self.threshold_capacity
        )

        if not done:
            if time > self.threshold_time:
                reward -= 1000
            if capacity == 0:
                reward += 1000
            reward += 1 / (euclidean_distance((x, y), (next_x, next_y)))
        else:
            logger.warn(
                "가방 터짐"
            )

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = (40, 60, 18, 0)
        self.node_check = [True for _ in range(len(self.node_size))]
        return np.array(self.state)

    def get_action(self, state):


