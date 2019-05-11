#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:07:56 2019

@author: fabian
"""

class TicTacToeGame:
    """A simple Tic Tac Toe Game"""
    def __init__(self, cbXStep, cbOStep, debug=False):
        self.debug = debug
        self.cbXStep = cbXStep
        self.cbOStep = cbOStep
        self.reset()


    def __nextStep(self):
        if self.xIsNext:
            self.cbXStep(self.squares, self.__step)
        else:
            self.cbOStep(self.squares, self.__step)


    def __step(self, i, resultHandler):
        """One step forward

        :param i: index for next placement
        :return: nextSituation, number, doneState
        """

        if self.done(): # If game is done
            if self.debug: print('game is done')
            return resultHandler(0, True, None)

        if not self.squares[i] == 'N': # In case gameplayer selects illegal field
            if self.debug: print('illegal field')
            return resultHandler(-1, False, self.__nextStep)

        if self.xIsNext:
            self.squares[i] = 'X'
        else:
            self.squares[i] = 'O'
        
        self.history.append(self.squares.copy())

        self.xIsNext = not self.xIsNext

        if self.__winner() == self.squares[i]:
            if self.debug: print('game is done,', self.squares[i], 'is winner')
            return resultHandler(1, True, None)

        if self.done(): # If game is done
            if self.debug: print('game is done')
            return resultHandler(0, True, None)

        return resultHandler(0, False, self.__nextStep)


    def __winner(self):
        winStates = [[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]
        for winState in winStates:
            if not self.squares[winState[0]] == 'N' and self.squares[winState[1]] == self.squares[winState[0]] and self.squares[winState[2]] == self.squares[winState[0]]:
                return self.squares[winState[0]]
        return None


    def done(self):
        if self.__winner():
            return True
        for sq in self.squares:
            if sq == 'N':
                return False
        return True


    def printHistory(self):
        for s in self.history:
            print(s)


    def reset(self):
        self.squares = []
        self.history = []
        self.xIsNext = True
        for i in range(9):
            self.squares.append('N')
        return self.__nextStep()
