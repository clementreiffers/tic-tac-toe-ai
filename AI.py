import random
from sklearn.neural_network import MLPClassifier

from TicTacToe import TicTacToe


class AI(TicTacToe):
    def __init__(self):
        super().__init__()
        self.current_history = []
        self.history_all_games = []
        self.clf = MLPClassifier(
            solver="lbfgs", alpha=1e-5, hidden_layer_sizes=(6, 2), random_state=1
        )

    def play_AI(self):
        while not (self.is_winner(self.J1) or self.is_winner(self.J2)):
            self.play(random.randint(0, 2), random.randint(0, 2), self.J1)
            self.play(random.randint(0, 2), random.randint(0, 2), self.J2)
