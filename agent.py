#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:53:57 2019

@author: fabian
"""
from tttsituation import TTTSituation
from ttthistory import TTTHistory
import numpy as np
import random
import pandas as pd


class Agent:
    def __init__(self, name, epsilon, discount, learning_rate, debug=False):
        self.__situations = []
        self.__history = []
        self.__currentSituationIndex = None
        self.__currentActionIndex = None
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
            return np.argmax(self.__lastSituation.getActions())

    def learnHistory(self):
        if self.debug: print('Learning History')
        steps = len(self.__history)
        step = steps-1
        while step >= 0:
            situation = self.__history[step].getSituation()
            reward = self.__history[step].getReward()
            actionIndex = self.__history[step].getActionIndex()
            if self.debug: print(situation.getSquares(), reward, actionIndex)
            if(step == steps-1):
                situation.setAction(actionIndex, reward)
            else:
                nextSituation = self.__history[step-1].getSituation()
                self.calcQ(situation, actionIndex, nextSituation, reward)
            step -= 1
        self.__history = []
        

    def saveForLearning(self, reward, done):
        if reward < 0:  # In case of illegal action
            self.__lastSituation.setAction(self.__lastActionIndex, reward)
            return

        self.__history.append(TTTHistory(self.__lastSituation, reward, self.__lastActionIndex))

    def calcQ(self, currentSituation, actionIndex, nextSituation, reward):
        next_q = reward + self.discount_factor * \
            np.max(nextSituation.getActions())
        actionQ = currentSituation.getAction(actionIndex)
        updateValue = (1-self.learning_rate) * actionQ + \
            self.learning_rate * next_q
        currentSituation.setAction(actionIndex, updateValue)

    def __findInSituations(self, targetSituation):
        for s in self.__situations:
            if s.compareTo(targetSituation):
                return s
        return None

    def decide(self, squares):
        ''' Function to decide what action should selected as next step 
            based on experience and randomness
        '''
        situation = TTTSituation(squares.copy(), np.zeros([9]))
        equalSituation = self.__findInSituations(situation)

        if equalSituation:
            self.__lastSituation = equalSituation
            self.__lastActionIndex = self.__get_greedy()
        else:
            self.__situations.append(situation)
            self.__lastSituation = situation
            self.__lastActionIndex = self.__get_greedy()
        return self.__lastActionIndex

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
            dL = list(s.getSquares().copy()) + \
                list(s.getActions().copy()) + list([s.howOften()])
            formed.append(dL)
        dfSituations = pd.DataFrame(formed)
        dfSituations.to_csv(file_path)

    def loadSituations(self, file_path=None):
        if not file_path:
            file_path = 'situations_' + self.__name + '.csv'
        dfLoaded = pd.read_csv(file_path, index_col=0)
        situations = []
        for s in dfLoaded.get_values():
            situations.append(TTTSituation(s[:9], s[9:18], s[18]))
        self.__situations = situations
