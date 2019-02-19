# This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a 
# state.GetRandomMove() or state.DoRandomRollout() function.
# 
# Example GameState classes for Nim, OXO and Othello are included to give some idea of how you
# can write your own GameState use UCT in your 2-player game. Change the game to be played in 
# the UCTPlayGame() function at the bottom of the code.
# 
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
# 
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
# 
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai

from math import *
from copy import deepcopy
import random
import timeit

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
        self.playerJustMoved = 2 # At the root pretend the player just moved is player 2 - player 1 has the first move
        self.previousMove = -1
        self.board = [[0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0]]
        
    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        st.previousMove = self.previousMove
        st.board = deepcopy(self.board)
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[board(move)][cell(move)] = self.playerJustMoved
        self.previousMove = cell(move)
        
    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        # No moves when someone wins
        for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if (Winner(self.board[x]) == Winner(self.board[y]) == Winner(self.board[z])) and (Winner(self.board[z]) != 0):
                return []

        if self.previousMove != -1 and Winner(self.board[cell(self.previousMove)]) == 0:
            return [toMove(self.previousMove, i) for i in range(9) if self.board[cell(self.previousMove)][i] == 0]
        else:
            moves = []
            for i in range(9):
                if Winner(self.board[i]) == 0:
                    moves.extend([toMove(i, j) for j in range(9) if self.board[i][j] == 0])
            return moves
    
    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm. 
        """
        for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if Winner(self.board[x]) == Winner(self.board[y]) == Winner(self.board[z]):
                if Winner(self.board[x]) == playerjm:
                    return 1.0
                else:
                    return 0.0
        if self.GetMoves() == []: return 0.5 # draw
        assert False

    def __repr__(self):
        """ Don't need this - but good style.
        """
        n_board = [[0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0]]

        for row in range(9):
            for i in range(3):
                for j in range(3):
                    n_board[row][i * 3 + j] = self.board[3 * (row // 3) + i][3 * (row % 3) + j]

        s= ""
        for i in range(9):
            if i % 3 == 0:
                s += "\n" 
            for j in range(9):
                if j % 3 == 0:
                    s += " "
                s += ".XO"[n_board[i][j]]
            s += "\n"
        return s

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        self.playerJustMoved = state.playerJustMoved # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)

    start = timeit.default_timer()
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        #print(i)
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves) 
            state.DoMove(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while True: # while state is non-terminal
            moves = state.GetMoves()
            if not moves:
                break
            state.DoMove(random.choice(moves))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    # Output some information about the tree - can be omitted
    # if (verbose): print(rootnode.TreeToString(0))
    # else: print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
                
def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number 
        of UCT iterations (= simulations = tree nodes).
    """
    print("Welcome to Ultimate Tic-Tac-Toe!")
    player = 1 if input("Do you want to go first? [Y/N]: ") == "Y" else 2
    print()

    state = GameState() # uncomment to play OXO
    while (state.GetMoves() != []):
        currentPlayer = 3 - state.playerJustMoved
        print("Moves for player " + str(currentPlayer) + ": " + str(state.GetMoves()) + "\n")
        if currentPlayer == player:
            # m = UCT(rootstate = state, itermax = 2000, verbose = False) # play with values for itermax and verbose = True
            m = int(input("Enter the cell you want to play: "))
        else:
            m = UCT(rootstate = state, itermax = 7000, verbose = False)
            print("Opponent played: " + str(m) + "\n")
        state.DoMove(m)
        print(str(state))
    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print("Player " + str(3 - state.playerJustMoved) + " wins!")
    else: print("Nobody wins!")

if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    UCTPlayGame()

            