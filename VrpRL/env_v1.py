import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

class Vrp(gym.Env):
    metadata = {
        pass
    }

    def __init__(self):
        pass

    def seed(self, seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step():
        pass

    def reset():
        pass

    def render():
        pass

    def close():
        pass