"""

on veut prédire le meilleur coup avec la config courante

1 2 1
2 1 2 = 2 1
0 2 1

"""
from TicTacToe import TicTacToe


def get_all_available_positions():
    return [[i, j] for i in range(3) for j in range(3)]


# class AI2(TicTacToe):
#     def __init__(self):
