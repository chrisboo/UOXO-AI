from UltimateTicTacToeAI import UCT
from UltimateTicTacToeLogic import GameState


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

            