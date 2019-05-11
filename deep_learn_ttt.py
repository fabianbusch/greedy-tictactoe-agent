#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 23:47:18 2019

@author: fabian
"""

import tensorflow as tf
from ttt import TicTacToeGame
from agent import Agent

agent1 = Agent('Agent1', 0.2, 0.95, 0.3)  
agent2 = Agent('Agent2', 1, 1, 0.8)     

game = TicTacToeGame(agent1.decide, agent2.decide)

