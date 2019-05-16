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

agent1.loadSituations()
agent2.loadSituations()

game = TicTacToeGame(agent1, agent2)

i = 0
while len(agent1.getSituations()) < math.pow(3, 9):
    '''There are 3^9 possible board situations...'''
    done = False
    
    if i % 100 == 0:
        print('EPISODE', i)

    if i % 1000 == 0:
        agent1.saveSituations()
        agent2.saveSituations()

    while not done:
        done = game.done()

    agent1.learnHistory()
    agent2.learnHistory()
    game.reset()
    i += 1