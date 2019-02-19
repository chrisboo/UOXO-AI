from copy import deepcopy


def board(move):
    return move // 9

def cell(move):
    return move % 9

def toMove(board, cell):
    return 9 * board + cell

def Winner(miniboard):
    for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if (miniboard[x] == miniboard[y] == miniboard[z]) and (miniboard[z] != 0):
            return miniboard[x]
    return 0

class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic
        zero-sum game, although they can be enhanced and made quicker, for example by using a
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """

    def __init__(self):
        self.playerJustMoved = 2  # At the root pretend the player just moved is player 2 - player 1 has the first move
        self.activeBoard = -1
        self.pieces = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.winnerOfBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.winner = 0

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        st.activeBoard = self.activeBoard
        st.pieces = deepcopy(self.pieces)
        st.winnerOfBoard = deepcopy(self.winnerOfBoard)
        st.winner = self.winner
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved
        self.pieces[board(move)][cell(move)] = self.playerJustMoved
        self.activeBoard = cell(move)

        maybe = False
        if Winner(self.pieces[board(move)]) == self.playerJustMoved:
            self.winnerOfBoard[board(move)] = self.playerJustMoved
            maybe = True

        if maybe:
            for (x, y, z) in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
                if (self.winnerOfBoard[x] == self.winnerOfBoard[y] == self.winnerOfBoard[z]) and (self.winnerOfBoard[z] != 0):
                    self.winner = self.winnerOfBoard[z]

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        # No moves when someone wins
        if self.winner != 0:
            return []

        if self.activeBoard != -1 and self.winnerOfBoard[cell(self.activeBoard)] == 0:
            return [toMove(self.activeBoard, i) for i in range(9) if self.pieces[cell(self.activeBoard)][i] == 0]
        else:
            moves = []
            for i in range(9):
                if self.winnerOfBoard[i] == 0:
                    moves.extend([toMove(i, j) for j in range(9) if self.pieces[i][j] == 0])
            return moves

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        for (x, y, z) in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if self.winnerOfBoard[x] == self.winnerOfBoard[y] == self.winnerOfBoard[z]:
                if self.winnerOfBoard[x] == playerjm:
                    return 1.0
                else:
                    return 0.0
        if self.GetMoves() == []: return 0.5  # draw
        assert False

    def __repr__(self):
        """ Don't need this - but good style.
        """
        n_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        for row in range(9):
            for i in range(3):
                for j in range(3):
                    n_board[row][i * 3 + j] = self.pieces[3 * (row // 3) + i][3 * (row % 3) + j]

        s = ""
        for i in range(9):
            if i % 3 == 0:
                s += "\n"
            for j in range(9):
                if j % 3 == 0:
                    s += " "
                s += ".XO"[n_board[i][j]]
            s += "\n"
        return s
