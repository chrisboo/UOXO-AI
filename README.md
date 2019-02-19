# Ultimate Tic-Tac-Toe Agent
An AI agent that plays the Ultimate Tic-Tac-Toe using Monte Carlo Tree Search (MCTS) and Upper Confidence Bounds (UCB).

# Game Play

```
python main.py 2000
```

where `2000` is the number of tree search iteration. A larger value increases the strength of the AI, as well as the time needed for it to make a decision. Suggested values are multiples of `1000`.

# Performance Benchmark

With an average decision time of 1 second, it plays `100-0` against a random player.

# Acknowledgement

The Monte Carlo Tree Search (MCTS) and Upper Confidence Bounds (UCB) implementation is modified from [MCTS.ai](http://mcts.ai/code/python.html).
