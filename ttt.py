#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:07:56 2019

TODO: Waterfall learning

@author: fabian
"""

class TicTacToeGame:
    """A simple Tic Tac Toe Game"""
    def __init__(self, player1, player2, debug=False):
        self.debug = debug
        self.player1 = player1
        self.player2 = player2
        self.reset()


    def __nextStep(self):
        if self.xIsNext:
            self.__doStep(self.player1.decide(self.squares), self.player1)
        else:
            self.__doStep(self.player2.decide(self.squares), self.player2)


    def __doStep(self, i, player):
        """One step forward

        :param i: index for next placement
        :return: nextSituation, number, doneState
        """

        if not self.squares[i] == 'N': # In case gameplayer selects illegal field
            if self.debug: print('illegal field')
            player.saveForLearning(-1, False)
            self.__nextStep()
            return

        if self.xIsNext:
            self.squares[i] = 'X'
        else:
            self.squares[i] = 'O'
        
        self.history.append(self.squares.copy())

        self.xIsNext = not self.xIsNext

        if self.__winner() == self.squares[i]:
            if self.debug: print('game is done,', self.squares[i], 'is winner')
            player.saveForLearning(1, True)
            return

        if self.done(): # If game is done
            if self.debug: print('game is done')
            player.saveForLearning(0, True)
            return

        player.saveForLearning(0, False)
        self.__nextStep()
        return


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
        print('Game history:')
        for s in self.history:
            print(s)


    def reset(self):
        self.squares = []
        self.history = []
        self.xIsNext = True
        for _ in range(9):
            self.squares.append('N')
        return self.__nextStep()
