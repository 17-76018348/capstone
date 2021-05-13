from math import *
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

import math
def euclidean_distance(pt1, pt2):
    distance = 0
    for i in range(len(pt1)):
        distance += (pt1[i] - pt2[i]) ** 2
    return distance ** 0.5


class VrpEnv(object):
    def __init__(self, x,y,cap):
        #self.customer_x = nodes['map_coored'][0]
        #self.customer_y = nodes['map_coored'][1]
        #self.capacity = nodes['capacity']
        self.customer_x = x
        self.customer_y = y
        self.capacity = cap
        
        self.node_size = 10
        self.depot_x = 40
        self.depot_y = 50
        self.speed = 70
        self.node_check = [True for _ in range(self.node_size)]

        self.threshold_capacity = 20
        self.threshold_time = 60 * 24
        self.x_threshold = 2.4
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        high = np.array([self.x_threshold * 2,
                         np.finfo(np.float32).max,
                         self.theta_threshold_radians * 2,
                         np.finfo(np.float32).max],
                        dtype=np.float32)
        self.action_space = spaces.Discrete(self.node_size)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        
        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action ):
        x, y, capacity, time, complete_requests = self.state
        next_x = self.customer_x[action]
        next_y = self.customer_y[action]
        self.node_check[action] = False

        next_time = time + (euclidean_distance((x, y), (next_x, next_y)) / self.speed)
        reward = 10
        capacity -= self.capacity[action]
        complete_requests += 1

        self.state = (next_x, next_y, capacity, next_time, complete_requests)

        done = bool(
            capacity < self.threshold_capacity
        )

        if done:
            if time > self.threshold_time:
                reward -= 1000
            # if capacity == 0:
            #     reward += 1000
            reward += 1 / (euclidean_distance((x, y), (next_x, next_y)) + 1)
        else:
            reward = 0
            logger.warn(
                "bag boom"
            )

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = (40, 50, 0, 0, 0)
        self.node_check = [True for _ in range(self.node_size)]
        return np.array(self.state)
