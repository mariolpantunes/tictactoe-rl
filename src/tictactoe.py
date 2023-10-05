# coding: utf-8

'''
TODO:
'''

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import pickle
import logging
import numpy as np


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TicTacToe:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.cols = 3
        self.rows = 3
        self.playerSymbol = 1
        self.board = np.zeros((self.cols, self.rows))
        self.isEnd = False
    
    def get_state(self):
        return self.board.flatten()
    
    
    def availablePositions(self):
        positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    def winner(self):
        # row
        for i in range(self.rows):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        # col
        for i in range(self.cols):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(self.cols)])
        diag_sum2 = sum([self.board[i, self.cols - i - 1] for i in range(self.cols)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None

    def play_action(self, position):
        if position in self.availablePositions():
            self.board[position] = self.playerSymbol
            # switch to another player
            self.playerSymbol = -1 if self.playerSymbol == 1 else 1
        else:
            logger.warning(f'Invalid position ({position}) from {self.playerSymbol}')

    # board reset
    def reset(self):
        self.board = np.zeros((self.rows, self.cols))
        self.isEnd = False
        self.playerSymbol = 1
    
    def play(self, rounds=10):
        win_p1, draws, win_p2 = 0, 0, 0
        
        
        for i in range(rounds):
            while not self.isEnd:
                # Player 1
                r, c, _ = self.p1.chooseAction(self.get_state(), self.playerSymbol)
                p1_action = (r, c)
                self.play_action(p1_action)

                win = self.winner()
                if win is not None:
                    self.reset()
                    if win == 1:
                        win_p1 += 1
                    elif win == -1:
                        win_p2 += 1
                    else:
                        draws += 1
                    break

                else:
                    # Player 2
                    r, c, _ = self.p2.chooseAction(self.get_state(), self.playerSymbol)
                    p2_action = (r, c)
                    self.play_action(p2_action)
                    
                    win = self.winner()
                    if win is not None:
                        self.reset()
                        
                        if win == 1:
                            win_p1 += 1
                        elif win == -1:
                            win_p2 += 1
                        else:
                            draws += 1
                        break
        
        return win_p1, draws, win_p2

