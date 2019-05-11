#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:30:42 2019

@author: fabian
"""

from ttt import TicTacToeGame
from agent import Agent
import math

agent1 = Agent('Agent1', 0.2, 0.95, 0.3)
agent2 = Agent('Agent2', 1, 1, 0.8)

game = TicTacToeGame(agent1.decide, agent2.decide)

EPISODE = 0

while len(agent1.getSituations()) < math.pow(3, 9):
    '''There are 3^9 possible board situations...'''
    done = False
    
    while not done:
        done = game.done()

    if EPISODE % 1000 == 0:
        print('Episode', EPISODE)
        agent1.saveSituations()
        agent2.saveSituations()

    game.reset()
    EPISODE += 1