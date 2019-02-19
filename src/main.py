import sys
import numpy as np

from UltimateTicTacToeAI import UCT
from UltimateTicTacToeLogic import GameState


def UCTPlayGame(itermax):
    """ Play a sample game between two UCT players where each player gets a different number 
        of UCT iterations (= simulations = tree nodes).
    """
    print("Welcome to Ultimate Tic-Tac-Toe!")
    player = 2 if input("Do you want to go first? [Y/N]: ") == "N" else 1

    state = GameState()
    while state.GetMoves():
        currentPlayer = state.NextPlayer()

        print(str(state))
        print("Moves for player " + str(currentPlayer) + ": ")
        print(np.matrix(state.GetMoves()), "\n")

        if currentPlayer == player:
            while m not in state.GetMoves():
                try:
                    m = int(input("Your move: "))
                except ValueError:
                    continue
            # m = random.choice(state.GetMoves())
        else:
            m = UCT(rootstate=state, itermax=itermax, verbose=False)
            print("AI played: " + str(m))
        state.DoMove(m)
    print(str(state))

    if state.GetResult(state.playerJustMove) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
        return state.playerJustMoved
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print("Player " + str(state.NextPlayer()) + " wins!")
        return state.NextPlayer()
    else:
        print("Nobody wins!")
        return 0


if __name__ == "__main__":

    itermax = int(sys.argv[1])

    UCTPlayGame(itermax)
