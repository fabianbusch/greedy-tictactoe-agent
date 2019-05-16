#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:59:16 2019

@author: fabian
"""


class TTTHistory:
    def __init__(self, situation, reward, actionIndex):
        self.__situation = situation
        self.__reward = reward
        self.__actionIndex = actionIndex

    def getSituation(self):
        return self.__situation

    def getReward(self):
        return self.__reward

    def getActionIndex(self):
        return self.__actionIndex
