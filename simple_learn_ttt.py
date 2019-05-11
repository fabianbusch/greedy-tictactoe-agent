#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:30:42 2019

@author: fabian
"""

from ttt import TicTacToeGame
from agent import Agent

agent1 = Agent('Agent1', 0.2, 0.95, 0.3)
agent2 = Agent('Agent2', 1, 1, 0.8)

game = TicTacToeGame(agent1.decide, agent2.decide)

EPISODES = 100000

for i in range(EPISODES):
    done = False
    
    while not done:
        done = game.done()

    if i % 1000 == 0:
        print('Episode', i, 'of', EPISODES)
        agent1.saveSituations()
        agent2.saveSituations()

    game.reset()
    
'''There are 3^9 possible board situations...'''