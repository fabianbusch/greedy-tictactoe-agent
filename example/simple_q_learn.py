#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 19:01:11 2019

@author: fabian
"""

import gym
import numpy as np
import random

env = gym.make('FrozenLake-v0')
Q = np.zeros([env.observation_space.n, env.action_space.n])

EPISODES = 40000
LEARNING_RATE = 0.3
DISCOUNT_FACTOR = 0.95
EPSILON = 0.2


def get_greedy(Q, s):
    if random.uniform(0, 1) < EPSILON:
        return env.action_space.sample()
    else:
        return max(list(range(env.action_space.n)), key=lambda x: Q[s, x])


for i in range(EPISODES):
    s = env.reset()

    done = False

    if i % 1000:
        print('Episode', i, 'of', EPISODES)

    while not done:
        a = get_greedy(Q, s)
        s_next, r, done, _ = env.step(a)
        print('r:', r)
        next_q = r + DISCOUNT_FACTOR * np.max(Q[s_next, :])
        Q[s, a] = (1-LEARNING_RATE) * Q[s, a] + LEARNING_RATE * next_q
        s = s_next

print(Q)
