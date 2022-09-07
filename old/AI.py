"""
THIS AI IS BASED ON WHICH GAME HAS PERMITTED A WIN OR A LOOSE
IT DOESN'T TAKE CONSIDERATION OF WHICH STEPS
"""

import copy
import random

import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from TicTacToe import TicTacToe


def change_value_x_y(x, y, value, lst):
    lst[x][y] = value
    return lst


def get_all_available_positions():
    return [[i, j] for i in range(3) for j in range(3)]


class AI(TicTacToe):
    def __init__(self):
        super().__init__()
        self.clf = DecisionTreeClassifier(criterion="entropy", random_state=1, max_depth=6)
        self.saved_bg, self.labels = [], []
        self.is_ai_trained = False
        self.way_to_win, self.config = [], []

    def play_ai(self, show_plateau):
        available_positions = get_all_available_positions()
        random.shuffle(available_positions)
        index = 0
        self.way_to_win = []
        while not self.is_winner(self.J1) and not self.is_winner(self.J2) and index < len(available_positions) - 1:
            if self.is_ai_trained:
                # AI
                coord = self.predict_position(available_positions)
                self.play(coord, self.J1, show_plateau=show_plateau)
                available_positions.remove(coord)

                # random play
                coord = available_positions[-1]
                self.play(coord, self.J2, show_plateau=show_plateau)
                available_positions.remove(coord)
            else:
                self.play(available_positions[index], self.J1, show_plateau=show_plateau)
                index += 1

                self.play(available_positions[index], self.J2, show_plateau=show_plateau)
                index += 1
        return self.is_winner(self.J1), self.is_winner(self.J2)

    def generate_end_games(self):
        epochs = 5
        nbr_game_epochs = 10000
        J1_win, J2_win, equality_win = 0, 0, 0
        for e in range(epochs + 1):
            for _ in range(nbr_game_epochs):
                is_J1_win, is_J2_win = self.play_ai(show_plateau=False)

                J1_win += is_J1_win and not is_J2_win
                J2_win += is_J2_win and not is_J1_win
                equality_win += is_J1_win and is_J2_win

                self.board_game = list(np.asarray(self.board_game).reshape(-1))
                if is_J1_win and not is_J2_win:
                    if all(val != self.board_game for val in self.saved_bg):
                        self.saved_bg.append(self.board_game)
                        self.labels.append(0)
                elif is_J2_win and not is_J1_win:
                    if all(val != self.board_game for val in self.saved_bg):
                        self.saved_bg.append(self.board_game)
                        self.labels.append(1)
                self.init_board_game()
            print(f"epochs : {e}/{epochs} generated : {len(self.saved_bg)}")
            print(f"J1 {J1_win}, AI {J2_win}")
            self.train()

    def train(self):
        x_train, x_test, y_train, y_test = train_test_split(self.saved_bg, self.labels, test_size=0.3, random_state=1)
        self.clf.fit(x_train, y_train)
        y_pred = self.clf.predict(x_test)
        # how did our model perform?
        count_misclassified = (y_test != y_pred).sum()
        print(f"Misclassified samples: {count_misclassified} / {len(x_test)}, nbr_bg = {len(self.saved_bg)}")
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print("Accuracy: {:.2f}".format(accuracy))
        self.is_ai_trained = True

    def get_copy_board_game(self):
        return copy.deepcopy(self.board_game)

    def generate_x_test(self, available_positions, player):
        return StandardScaler().fit_transform(
            np.array(
                [
                    np.asarray(change_value_x_y(x, y, player, self.get_copy_board_game())).reshape(-1)
                    for x, y in available_positions
                ]
            )
        )

    def predict_position(self, available_positions):
        proba = self.clf.predict_proba(self.generate_x_test(available_positions, self.J2))
        return available_positions[np.argmax(proba)]

    def play_against_ai(self):
        self.generate_end_games()
        available_positions = get_all_available_positions()
        random.shuffle(available_positions)
        index = 0
        replay = True
        while replay:
            while not self.is_winner(self.J1) and not self.is_winner(self.J2) and index < len(available_positions) - 1:
                # for AI
                x, y = self.predict_position(available_positions)

                print("IA DECIDE", x, y)
                self.play([x, y], self.J2, show_plateau=True)
                available_positions.remove([x, y])

                # for human
                x, y, playable = None, None, False
                while not playable:
                    x = int(input("give x coordinate between 0 and 2 \n>>>"))
                    y = int(input("give y coordinate between 0 and 2 \n>>>"))
                    playable = 0 <= x <= 2 and 0 <= y <= 2 and self.board_game[x][y] == 0
                self.play([x, y], self.J1, show_plateau=True)
                try:
                    available_positions.remove([x, y])
                except:
                    print(f"cannot remove {[x, y]} {available_positions}")
            self.init_board_game()
            replay = input("replay ?(y/n)") == "y"
