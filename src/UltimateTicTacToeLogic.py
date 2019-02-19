from copy import deepcopy


class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic
        zero-sum game, although they can be enhanced and made quicker, for example by using a
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """

    WINNING_COMBINATIONS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    @classmethod
    def Board(cls, move):
        return move // 9

    @classmethod
    def Position(cls, move):
        return move % 9

    @classmethod
    def ToMove(cls, board, cell):
        return board * 9 + cell

    def __init__(self):
        self.playerJustMoved = 2  # At the root pretend the player just moved is player 2 - player 1 has the first move
        self.activeBoard = None
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
        self.winnerOfGame = 0

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        st.activeBoard = self.activeBoard
        st.pieces = deepcopy(self.pieces)
        st.winnerOfBoard = deepcopy(self.winnerOfBoard)
        st.winnerOfGame = self.winnerOfGame
        return st

    def NextPlayer(self):
        return 3 - self.playerJustMoved

    def GetWinner(self, boardID):
        board = self.pieces[boardID]
        for (x, y, z) in GameState.WINNING_COMBINATIONS:
            if board[x] == board[y] == board[z] != 0:
                return board[x]
        return 0

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        board = GameState.Board(move)
        position = GameState.Position(move)

        self.playerJustMoved = self.NextPlayer()
        self.pieces[board][position] = self.playerJustMoved
        self.activeBoard = position

        if self.GetWinner(board) == self.playerJustMoved:
            self.winnerOfBoard[board] = self.playerJustMoved
            for (x, y, z) in GameState.WINNING_COMBINATIONS:
                if self.winnerOfBoard[x] == self.winnerOfBoard[y] == self.winnerOfBoard[z] != 0:
                    self.winnerOfGame = self.winnerOfBoard[z]

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        # No moves when someone wins
        if self.winnerOfGame != 0:
            return []

        if self.activeBoard is not None and self.winnerOfBoard[self.activeBoard] == 0:
            moves = [GameState.ToMove(self.activeBoard, i) for i in range(9) if self.pieces[self.activeBoard][i] == 0]
            if moves:
                return moves

        moves = []
        for i in range(9):
            if self.winnerOfBoard[i] == 0:
                moves.extend([GameState.ToMove(i, j) for j in range(9) if self.pieces[i][j] == 0])
        return moves

    def GetResult(self, playerJustMoved):
        """ Get the game result from the viewpoint of playerJustMoved.
        """
        if self.winnerOfGame == playerJustMoved:
            return 1.0
        elif self.winnerOfGame == 0 and not self.GetMoves():
            return 0.5
        else:
            return 0.0

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
