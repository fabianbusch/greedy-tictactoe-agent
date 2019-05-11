#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:53:57 2019

@author: fabian
"""
from tttsituation import TTTSituation
import numpy as np
import random
import pandas as pd


class Agent:
    def __init__(self, name, epsilon, discount, learning_rate, debug=False):
        self.__situations = []
        self.__currentSituationIndex = None
        self.__lastActionIndex = None
        self.debug = debug
        self.epsilon = epsilon
        self.discount_factor = discount
        self.learning_rate = learning_rate
        self.__name = name
        return

    def __get_greedy(self):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 8)
        else:
            return np.argmax(self.__situations[self.__currentSituationIndex].getActions())

    def chooseAction(self, squares):
        situation = TTTSituation(squares.copy(), np.zeros([9]))
        if self.debug:
            self.printSituations()
        sI = 0
        while sI < len(self.__situations):
            if self.__situations[sI].compareTo(situation):
                self.__currentSituationIndex = sI
                self.__lastActionIndex = self.__get_greedy()
                if self.debug:
                    print('Found an equal situation:',
                          self.__situations[sI].getSquares())
                if self.debug:
                    print('Choosing Field', self.__lastActionIndex,
                          'for Board:', situation.getSquares())
                return self.__lastActionIndex
            sI = sI + 1
        if self.debug:
            print('Saving unkown Situation:', situation.getSquares())
        self.__situations.append(situation)
        self.__currentSituationIndex = len(self.__situations) - 1
        self.__lastActionIndex = self.__get_greedy()
        if self.debug:
            print('Choosing Field', self.__lastActionIndex,
                  'for Board:', situation.getSquares())
        return self.__lastActionIndex

    def __resultHandler(self, reward, done, readyCallback):
        if self.debug:
            print("Handling Result")
        if self.debug:
            print('\n')
        next_q = reward + self.discount_factor * \
            np.max(
                self.__situations[self.__currentSituationIndex].getActions())
        tmpReward = self.__situations[self.__currentSituationIndex].getAction(
            self.__lastActionIndex)
        updateValue = (1-self.learning_rate) * tmpReward + \
            self.learning_rate * next_q
        self.__situations[self.__currentSituationIndex].setAction(
            self.__lastActionIndex, updateValue)
        if not done:
            readyCallback()
        return

    def decide(self, squares, stepCallback):
        stepCallback(self.chooseAction(squares), self.__resultHandler)
        return

    def getSituations(self):
        return self.__situations

    def printSituations(self):
        print('My Situations:')
        for s in self.__situations:
            s.printSituation()

    def saveSituations(self, file_path=None):
        if not file_path:
            file_path = 'situations_' + self.__name + '.csv'
        formed = []
        for s in self.__situations:
            dL = list(s.getSquares().copy()) + list(s.getActions().copy()) + list([s.howOften()])
            formed.append(dL)
        dfSituations = pd.DataFrame(formed)
        dfSituations.to_csv(file_path)

    def loadSituations(self, file_path=None):
        if not file_path:
            file_path = 'situations_' + self.__name + '.csv'
        dfLoaded = pd.read_csv(file_path, index_col=0)
        situations = []
        for s in dfLoaded.get_values():
            situations.append(TTTSituation(s[:9], s[9:17], s[17]))
        self.__situations = situations
