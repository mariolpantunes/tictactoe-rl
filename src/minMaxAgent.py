import math
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)



class MinMaxAgent:
    def __init__(self, mem=None):
        if mem is not None:
            self._chooseAction = mem.cache(self._chooseAction)
        else:
            self._chooseAction = self._chooseAction

    @staticmethod
    def _isMovesLeft(board) :  
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if (board[i][j] == 0) : 
                    return True 
        return False

    @staticmethod
    def _available_positions(current_state):
        positions = []
        for i in range(len(current_state)):
            if current_state[i] == 0:
                r = int(i / self.cols)
                c = i % self.cols
                positions.append((r, c))
        return positions

    @staticmethod
    def _evaluate(board, player):
        opponent = -player
        # Checking for Rows for X or O victory.  
        for row in range(board.shape[0]):      
            if (board[row][0] == board[row][1] and board[row][1] == board[row][2]):         
                if (board[row][0] == player) : 
                    return 10
                elif (board[row][0] == opponent) : 
                    return -10

        # Checking for Columns for X or O victory.  
        for col in range(board.shape[1]): 
            if (board[0][col] == board[1][col] and board[1][col] == board[2][col]): 
                if (board[0][col] == player):  
                    return 10
                elif (board[0][col] == opponent): 
                    return -10

        # Checking for Diagonals for X or O victory.  
        if (board[0][0] == board[1][1] and board[1][1] == board[2][2]): 
            if (board[0][0] == player) : 
                return 10
            elif (board[0][0] == opponent) : 
                return -10

        if (board[0][2] == board[1][1] and board[1][1] == board[2][0]): 
            if (board[0][2] == player): 
                return 10
            elif (board[0][2] == opponent): 
                return -10

        # Else if none of them have won then return 0  
        return 0

    @staticmethod
    def _minimax(board, player , depth, isMax, alpha, beta):
        score = MinMaxAgent._evaluate(board, player)
        opponent = -player

        # If Maximizer has won the game return his/her  
        # evaluated score  
        if (score == 10):
            return score 

        # If Minimizer has won the game return his/her  
        # evaluated score  
        if (score == -10):
            return score 

        # If there are no more moves and no winner then  
        # it is a tie  
        if (MinMaxAgent._isMovesLeft(board) == False):
            return 0

        # If this maximizer's move  
        if (isMax) :      
            best = -math.inf
            # Traverse all cells  
            for i in range(board.shape[0]):
                for j in range(board.shape[1]):
                    # Check if cell is empty  
                    if (board[i][j]==0): 
                        # Make the move
                        board[i][j] = player
                        # Call minimax recursively and choose
                        eval_score = MinMaxAgent._minimax(board, player, depth + 1, not isMax, alpha, beta)
                        # the maximum value  
                        best = max(best, eval_score)
                        # Undo the move  
                        board[i][j] = 0
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
            return best 

        # If this minimizer's move  
        else : 
            best = math.inf
            # Traverse all cells  
            for i in range(board.shape[0]):
                for j in range(board.shape[1]):
                    # Check if cell is empty  
                    if (board[i][j] == 0):
                        # Make the move  
                        board[i][j] = opponent  
                        # Call minimax recursively and choose
                        eval_score = MinMaxAgent._minimax(board, player, depth + 1, not isMax, alpha, beta)
                        # the minimum value  
                        best = min(best, eval_score) 
                        # Undo the move  
                        board[i][j] = 0
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            return best

    @staticmethod
    def _chooseAction(current_state, symbol):
        board = current_state.reshape(3, 3)
        bestVal = -1000 
        bestMove = (-1, -1)

        #logger.info(f'{board}')

        for i in range(board.shape[0]):
            for j in range(board.shape[1]):

                # Check if cell is empty  
                if (board[i][j] == 0) :  

                    # Make the move  
                    board[i][j] = symbol 

                    # compute evaluation function for this  move.
                    #key = ''.join(board.flatten().astype(int).astype(str)) + str(symbol)
                    #if key in self.table:
                    #    moveVal = self.table[key]
                    #else:
                    moveVal = MinMaxAgent._minimax(board, symbol, 0, False, -math.inf, math.inf)
                    #self.table[key] = moveVal

                    # Undo the move  
                    board[i][j] = 0

                    if (moveVal > bestVal) :                 
                        bestMove = (i, j) 
                        bestVal = moveVal

        r, c = bestMove
        return r, c, None

    def chooseAction(self, current_state, symbol):
        return self._chooseAction(current_state, symbol)
