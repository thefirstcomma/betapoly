import gym
# import numpy as np
import os, subprocess, time, signal
from gym import error, spaces
from gym import utils
from gym.utils import seeding
from gym_monopoly.game.game import Game


class MonopolyEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    # change here, if needed
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(MonopolyEnv, self).__init__()
        self.env = Game()
        self.players = []
        self.observation_space = spaces.Box(low=-1, high=1,
                                            shape=(self.env.getStateSize()))
        self.action_space = spaces.Tuple((spaces.Discrete(3),
                                          spaces.Box(low=0, high=100, shape=1),
                                          spaces.Box(low=-180, high=180, shape=1),
                                          spaces.Box(low=-180, high=180, shape=1),
                                          spaces.Box(low=0, high=100, shape=1),
                                          spaces.Box(low=-180, high=180, shape=1)
                                        ))
        # self.prev_action = None

    def step(self, action):
        self.env.action_helper(action)
        obs = self.env.get_state()
        reward = self.get_reward()
        done = self.env.game_over()
        return obs, reward, done, {}
        # return observation, reward, done, info

    
    # indexes of the list of action {
    #     0 : Type For ACTION_LOOKUP
    #     1 : PAY 50 FOR JAIL (0)/ ROLL DOUBLE (1)/ USE G.O.O.J CARD (2)
    #     2 : BUY / DONT BUY INDEX PROPERTY LANDED ON
    #     3 : BUY HOUSE ON THIS INDEX
    #     4 : SELL HOUSE ON THIS INDEX
    #     5 : MORTGAGE ON THIS INDEX
    #     6 : UN-MORTGAGE ON THIS INDEX
    #     7 : TRADE WITH PLAYER NUMBER
    #     8 : MONEY YOU GIVE
    #     9 : MONEY YOU TAKE
    #     10 : PROPERTY YOU GIVE
    #     11 : PROPERTY YOU GET
    #     12 : AUCTION AMOUNT # if == None or 0, quit auction
    #     13 : ACCEPT_TRADE
    # }

    # def take_action(self, action):
        # action_type = ACTION_LOOKUP[action[0]]
        # if action_type == 'BUY_PROPERTY_LANDED':
        #     self.env.act(action_type, action[2])
        # elif action_type == 'IN_JAIL_ACTION':
        #     self.env.act(action_type, action[1])
        # elif action_type == 'CONTINUE_AUCTION':
        #     self.env.act(action_type, action[12])
        # elif action_type == 'ACCEPT_TRADE':
        #     self.env.act(action_type, action[13])
        # elif action_type == 'MORTGAGE':
        #     self.env.act(action_type, action[5])
        # elif action_type == 'UNMORTGAGE':
        #     self.env.act(action_type, action[6])
        # elif action_type == 'TRADE':
        #     self.env.act(action_type, action[7], action[8], action[9], action[10], action[11])
        # elif action_type == 'BUY_HOUSE':
        #     self.env.act(action_type, action[3])
        # elif action_type == 'SELL_HOUSE':
        #     self.env.act(action_type, action[4])
        # else:
        #     print('Unrecognized action %d' % action_type)
    
    # Reward only for winning?
    def get_reward(self):
        if self.status == self.env.WON_MONOPOLY:
            return 1
        else:
            return -1

    def reset(self):
        observation = self.env.reset()
        return observation  # reward, done, info can't be included

    def render(self):
        self.env.print_info()

    # Nothing here since no actual gui
    def close(self):
        pass


ACTION_LOOKUP = {
    0 : 'BUY_PROPERTY_LANDED',
    1 : 'IN_JAIL_ACTION',
    2 : 'CONTINUE_AUCTION',
    3 : 'ACCEPT_TRADE',
    4 : 'MORTGAGE',
    5 : 'UNMORTGAGE',
    6 : 'TRADE',
    7 : 'BUY_HOUSE',
    8 : 'SELL_HOUSE',
    8 : 'END',
    9 : 'ROLL-DICE'
}

