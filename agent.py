#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:53:57 2019

@author: fabianbusch
"""
from __future__ import absolute_import, division, print_function
from tttsituation import TTTSituation
from ttthistory import TTTHistory
import numpy as np
import random
import pandas as pd

import tensorflow as tf

tf.enable_eager_execution()

class Agent:
    def __init__(self, name, epsilon, discount, learning_rate, debug=False, deepLearn=False):
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
        self.__deepLearn = deepLearn
        self.__model = tf.keras.Sequential([
            tf.keras.layers.Dense(27, input_shape=(27,)),
            tf.keras.layers.Dense(18),
            tf.keras.layers.Dense(9)
        ])
        self.__optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        self.__lossHistory = []
        return

    def __get_greedy(self):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 8)
        elif self.__deepLearn:
            return np.argmax(self.__model(self.__oneHot(self.__lastSituation.getSquares())))
        else:
            return np.argmax(self.__lastSituation.getActions())

    def __learnDeep(self):
        steps = len(self.__history)
        step = steps-1

        while step >= 0:
            if self.debug:
                print('Learning Step', step)

            situation = self.__history[step].getSituation()
            reward = self.__history[step].getReward()
            actionIndex = self.__history[step].getActionIndex()

            if (step == steps-1):  # In case we are at the last step in history
                max_q_next = 0
            else:
                nextSituation = self.__history[step-1].getSituation()
                next_q = self.__model(
                    self.__oneHot(nextSituation.getSquares()))
                max_q_next = np.max(next_q)

            squares = self.__oneHot(situation.getSquares())

            if self.debug:
                print('Squares:', squares)

            all_q = self.__model(squares)
            target_q = all_q.numpy()
            target_q[0, actionIndex] = reward + \
                self.discount_factor * max_q_next

            with tf.GradientTape() as tape:
                predicted_q = self.__model(squares, training=True)
                loss_value = tf.reduce_sum(tf.square(target_q - predicted_q))

            grads = tape.gradient(loss_value, self.__model.trainable_variables)
            self.__optimizer.apply_gradients(zip(grads, self.__model.trainable_variables),
                                      global_step=tf.train.get_or_create_global_step())
            self.__lossHistory.append(loss_value.numpy())
            
            step -= 1

        self.__history = []

    def __oneHot(self, squares):
        if self.debug: print(squares)
        arr = np.zeros(27)
        if self.debug: print(arr)
        square = 0
        for arrPlace in range(0, len(arr), 3):
            if self.debug: print('For', square, 'with value', squares[square])
            if squares[square] == 'N':
                arr[arrPlace] = 1
                if self.debug: print('Arr', arrPlace, 'is value', arr[arrPlace])
            elif squares[square] == 'X':
                arr[arrPlace+1] = 1
                if self.debug: print('Arr', arrPlace+1, 'is value', arr[arrPlace+1])
            elif squares[square] == 'O':
                arr[arrPlace+2] = 1
                if self.debug: print('Arr', arrPlace+2, 'is value', arr[arrPlace+2])
            square += 1
        if self.debug: print(arr)
        return tf.convert_to_tensor([arr], np.float32)

    def learnHistory(self):
        if self.debug:
            print('Learning History')
        if self.__deepLearn:
            return self.__learnDeep()

        steps = len(self.__history)
        step = steps-1
        while step >= 0:
            situation = self.__history[step].getSituation()
            reward = self.__history[step].getReward()
            actionIndex = self.__history[step].getActionIndex()
            if self.debug:
                print(situation.getSquares(), reward, actionIndex)
            if(step == steps-1):
                situation.setAction(actionIndex, reward)
            else:
                nextSituation = self.__history[step-1].getSituation()
                self.calcQ(situation, actionIndex, nextSituation, reward)
            step -= 1
        self.__history = []

    def saveForLearning(self, reward, done):
        ''' Saves last situation, last action choice and the reward in an internal history stack.
            The game should call this function immedialy in any case of an available feedback.
            If agent chose some illegal action, pass reward=-1
        '''
        if self.__learnDeep:
            return self.__saveForDeepLearning(reward, done)

        if reward < 0:  # In case of illegal action
            self.__lastSituation.setAction(self.__lastActionIndex, reward)
            return

        self.__history.append(TTTHistory(
            self.__lastSituation, reward, self.__lastActionIndex))

    def __saveForDeepLearning(self, reward, done):
        if reward < 0:  # In case of illegal action

            squares = self.__oneHot(self.__lastSituation.getSquares())
            all_q = self.__model(squares)
            target_q = all_q.numpy()
            target_q[0, self.__lastActionIndex] = reward

            with tf.GradientTape() as tape:
                predicted_q = self.__model(squares, training=True)
                loss_value = tf.reduce_sum(tf.square(target_q - predicted_q))

            grads = tape.gradient(loss_value, self.__model.trainable_variables)
            self.__optimizer.apply_gradients(zip(grads, self.__model.trainable_variables),
                                      global_step=tf.train.get_or_create_global_step())
            self.__lossHistory.append(loss_value.numpy())
            return

        self.__history.append(TTTHistory(
            self.__lastSituation, reward, self.__lastActionIndex))

    def calcQ(self, currentSituation, actionIndex, nextSituation, reward):
        ''' Used to update the current situations action-best-choice-table
        '''
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
        if self.__deepLearn:
            return self.__decideDeep(squares)

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

    def __decideDeep(self, squares):
        ''' Function to decide based on the trained NN
        '''
        situation = TTTSituation(squares.copy(), np.zeros([9]))
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

    def getName(self):
        return self.__name

    def getModel(self):
        return self.__model

    def getLossHistory(self):
        return self.__lossHistory