import gym
from gym import spaces
# import numpy as np
import os, subprocess, time, signal
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import game

# gym.make('gym_monopoly:monopoly-v0')

class MonopolyEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    #   Optional change here
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(MonopolyEnv, self).__init__()
        self.env = Game().run()

        self.action_space = gym.spaces.Box(0, 60, shape=(2,), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(np.int8(0), np.int8(-1), shape=(11, 11), dtype=np.int8)

    def step(self, action):
        self.take_action(action)
        self.status = self.env.step()
        reward = self.get_reward()
        ob = self.env.getState()
        episode_over = self.status != monopoly.IN_GAME
        return ob, reward, episode_over, {}
        # return observation, reward, done, info
    
    def take_action(self, action):
        """ Converts the action space into an HFO action. """
        action_type = ACTION_LOOKUP[action[0]]
        if action_type == hfo_py.DASH:
            self.env.act(action_type, action[1], action[2])
        elif action_type == hfo_py.TURN:
            self.env.act(action_type, action[3])
        elif action_type == hfo_py.KICK:
            self.env.act(action_type, action[4], action[5])
        else:
            print('Unrecognized action %d' % action_type)
            self.env.act(hfo_py.NOOP)
    
    def get_reward(self):
        """ Reward is given for winning? """
        if self.status == hfo_py.GOAL:
            return 1
        else:
            return 0

    def reset(self):
        return observation  # reward, done, info can't be included

    def render(self, mode='human'):
        pass

    def close(self):
        pass


ACTION_LOOKUP = {
    0 : hfo_py.DASH,
    1 : hfo_py.TURN,
    2 : hfo_py.KICK,
    3 : hfo_py.TACKLE,
    4 : hfo_py.CATCH,
}