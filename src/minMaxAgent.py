import math
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class MinMaxAgent:
    def __init__(self):
        self.rows = 3
        self.cols = 3

    def _isMovesLeft(self, board) :  
        for i in range(self.rows) : 
            for j in range(self.cols) : 
                if (board[i][j] == 0) : 
                    return True 
        return False

    def _available_positions(self, current_state):
        positions = []
        for i in range(len(current_state)):
            if current_state[i] == 0:
                r = int(i / self.cols)
                c = i % self.cols
                positions.append((r, c))
        return positions

    def _evaluate(self, board, player):
        opponent = -player
        # Checking for Rows for X or O victory.  
        for row in range(self.rows):      
            if (board[row][0] == board[row][1] and board[row][1] == board[row][2]):         
                if (board[row][0] == player) : 
                    return 10
                elif (board[row][0] == opponent) : 
                    return -10

        # Checking for Columns for X or O victory.  
        for col in range(self.cols): 
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

    def _minimax(self, board, player , depth, isMax, alpha, beta) :  
        score = self._evaluate(board, player)
        opponent = -player

        # If Maximizer has won the game return his/her  
        # evaluated score  
        if (score == 10) :  
            return score 

        # If Minimizer has won the game return his/her  
        # evaluated score  
        if (score == -10) : 
            return score 

        # If there are no more moves and no winner then  
        # it is a tie  
        if (self._isMovesLeft(board) == False) : 
            return 0

        # If this maximizer's move  
        if (isMax) :      
            best = -math.inf
            # Traverse all cells  
            for i in range(self.rows):          
                for j in range(self.cols): 
                    # Check if cell is empty  
                    if (board[i][j]==0): 
                        # Make the move
                        board[i][j] = player
                        # Call minimax recursively and choose
                        eval_score = self._minimax(board, player, depth + 1, not isMax, alpha, beta)
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
            for i in range(self.rows) :          
                for j in range(self.cols):
                    # Check if cell is empty  
                    if (board[i][j] == 0):
                        # Make the move  
                        board[i][j] = opponent  
                        # Call minimax recursively and choose
                        eval_score = self._minimax(board, player, depth + 1, not isMax, alpha, beta)
                        # the minimum value  
                        best = min(best, eval_score) 
                        # Undo the move  
                        board[i][j] = 0
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            return best

    def chooseAction(self, current_state, symbol):
        board = current_state.reshape(3,3)
        bestVal = -1000 
        bestMove = (-1, -1)

        #logger.info(f'{board}')

        for i in range(self.rows) :      
            for j in range(self.cols) : 

                # Check if cell is empty  
              if (board[i][j] == 0) :  

                  # Make the move  
                  board[i][j] = symbol 

                  # compute evaluation function for this  move.  
                  moveVal = self._minimax(board, symbol, 0, False, -math.inf, math.inf)  

                  # Undo the move  
                  board[i][j] = 0

                  if (moveVal > bestVal) :                 
                      bestMove = (i, j) 
                      bestVal = moveVal

        r,c = bestMove
        return r, c, None
