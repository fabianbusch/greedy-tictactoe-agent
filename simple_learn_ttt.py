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
    
    if i % 1000 == 0:
        print('Episode', i, 'of', EPISODES)
        sit1 = agent1.getSituations()
        sit2 = agent2.getSituations()
        print('Agent1 with', len(sit1), 'Agent2 with', len(sit2), 'Situations')
    
    while not done:
        done = game.done()
  
    game.reset()

# Checking if all situations are different

sit1 = agent1.getSituations()
sI = 0
for s in sit1:
    aI = 0
    for a in sit1:
        if s.compareTo(a) and not sI == aI:
            print('sI', sI, 'aI', aI)
        aI += 1
    sI += 1
            
    
# There are 3^9 possible board situations...