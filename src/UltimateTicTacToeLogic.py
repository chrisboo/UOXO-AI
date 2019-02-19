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
        self.previousMove = -1
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.won = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.winner = 0

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        st.previousMove = self.previousMove
        st.board = deepcopy(self.board)
        st.won = deepcopy(self.won)
        st.winner = self.winner
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[board(move)][cell(move)] = self.playerJustMoved
        self.previousMove = cell(move)

        maybe = False
        if Winner(self.board[board(move)]) == self.playerJustMoved:
            self.won[board(move)] = self.playerJustMoved
            maybe = True

        if maybe:
            for (x, y, z) in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
                if (self.won[x] == self.won[y] == self.won[z]) and (self.won[z] != 0):
                    self.winner = self.won[z]

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        # No moves when someone wins
        if self.winner != 0:
            return []

        if self.previousMove != -1 and self.won[cell(self.previousMove)] == 0:
            return [toMove(self.previousMove, i) for i in range(9) if self.board[cell(self.previousMove)][i] == 0]
        else:
            moves = []
            for i in range(9):
                if self.won[i] == 0:
                    moves.extend([toMove(i, j) for j in range(9) if self.board[i][j] == 0])
            return moves

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        for (x, y, z) in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if self.won[x] == self.won[y] == self.won[z]:
                if self.won[x] == playerjm:
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
                    n_board[row][i * 3 + j] = self.board[3 * (row // 3) + i][3 * (row % 3) + j]

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
