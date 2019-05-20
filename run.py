#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:30:42 2019

@author: fabianbusch
"""

from ttt import TicTacToeGame
from agent import Agent
import matplotlib.pyplot as plt
import math

agent1 = Agent('Agent1', 0.3, 1, 0.001, deepLearn=True, debug=False)
agent2 = Agent('Agent2', 1, 1, 0.1)

#agent1.loadSituations()
agent2.loadSituations()

game = TicTacToeGame(agent1, agent2)

EPISODES = 10000

i = 0
while i < EPISODES:
    '''There are 3^9 possible board situations...'''
    done = False
    
    if i % 100 == 0:
        print('EPISODE', i, 'of', EPISODES)

    if i % 1000 == 0:
        #agent1.saveSituations()
        agent2.saveSituations()

    while not done:
        done = game.done()

    agent1.learnHistory()
    agent2.learnHistory()
    game.reset()
    i += 1

lossHistory = agent1.getLossHistory()

plt.plot(lossHistory)
plt.show()