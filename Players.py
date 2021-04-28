'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

from operator import attrgetter

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MoveNode():
    def __init__(self, column, rownum, utility, board):
        self.col = column
        self.row = rownum
        self.utility = utility
        self.board = board  # Does not do a deep copy, must do a clone of another board or create a new one to input

    # def __gt__(self, other):
    #     if (self.utility > other.utility):
    #         return True
    #     else:
    #         return False

    # def __lt__(self, other):
    #     if (self.utility < other.utility):
    #         return True
    #     else:
    #         return False


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'

    def get_move(self, board):
        allSuccessors = self.generate_successors(self.symbol, board)
        for x in allSuccessors:
            print("Row: ", x.row, " Column: ", x.col, " Utility: ", x.utility)
        optimalState = min(allSuccessors, key=attrgetter('utility'))
        return (optimalState.col, optimalState.row)

    def generate_successors(self, currentSymbol, board):   
        allSuccessors = [] 
        for c in range (0, board.cols):
            for r in range (0, board.rows):
                if board.is_legal_move(c, r, currentSymbol):
                    newBoard = board.cloneOBoard()
                    newBoard.play_move(c, r, currentSymbol)
                    node = MoveNode(c, r, self.get_utility(newBoard), newBoard)
                    allSuccessors.append(node)

        if (currentSymbol == self.symbol):
            if (len(allSuccessors) == 0 and board.has_legal_moves_remaining(self.oppSym)):
                finalState = MoveNode(-1, -1, -1, board)
                
                newSuccessors = self.generate_successors(self.oppSym, board)
                finalState.utility = (max(newSuccessors, key=attrgetter('utility'))).utility
                allSuccessors.append(finalState)
                ## Create a situation for if the current player has no moves left but the opposing player does

            else:
                for x in allSuccessors:
                    if (x.utility == None):
                        newSuccessors = self.generate_successors(self.oppSym, x.board)
                        x.utility = (max(newSuccessors, key=attrgetter('utility'))).utility

        else:
            if (len(allSuccessors) == 0 and board.has_legal_moves_remaining(self.symbol)):
                finalState = MoveNode(-1, -1, -1, board)
                
                newSuccessors = self.generate_successors(self.symbol, board)
                finalState.utility = (min(newSuccessors, key=attrgetter('utility'))).utility
                allSuccessors.append(finalState)
            ## Create a situation for if the current player has no moves left but the opposing player does 

            else:
                for x in allSuccessors:
                    if (x.utility == None):
                        newSuccessors = self.generate_successors(self.symbol, x.board)  
                        x.utility = (min(newSuccessors, key=attrgetter('utility'))).utility
        
        return allSuccessors

    def get_utility(self, board):
        if (board.has_legal_moves_remaining(self.symbol) or board.has_legal_moves_remaining(self.oppSym)):
            return None
        else:
            return board.count_score(self.oppSym)       
        





