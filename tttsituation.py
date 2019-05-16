#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:59:16 2019

@author: fabian
"""


class TTTSituation:
    def __init__(self, squares, actions, happened=1):
        self.__squares = squares
        self.__actions = actions
        self.__happen = happened

    def getSquares(self):
        return self.__squares

    def getSquare(self, index):
        return self.__squares[index]

    def getActions(self):
        return self.__actions

    def getAction(self, index):
        return self.__actions[index]

    def setAction(self, index, value):
        self.__happened()
        self.__actions[index] = value

    def compareTo(self, otherSituation):
        i = 0
        while i < len(self.__squares):
            if not self.getSquare(i) == otherSituation.getSquare(i):
                return False
            i += 1
        return True

    def printSituation(self):
        print(self.__squares)

    def __happened(self):
        self.__happen += 1

    def howOften(self):
        return self.__happen
