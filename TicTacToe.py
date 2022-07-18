def is_winner_in_list(list, player):
    return any(line == [player] * 3 for line in list)


class TicTacToe:
    def __init__(self):
        self.boardGame = [["-" for _ in range(3)] for _ in range(3)]

        self.J1 = "X"
        self.J2 = "O"

    def launch_game(self):
        while not (self.is_winner(self.J1) or self.is_winner(self.J2)):
            self.show_game()
            self.play(self.J1)
            if self.is_winner(self.J1):
                print("J1 win !")
                break
            self.show_game()
            self.play(self.J2)
            if self.is_winner(self.J2):
                print("J2 win !")
                break

    def show_game(self):
        print("-" * 13)
        for line in self.boardGame:
            for value in line:
                print(f"| {value} ", end="")
            print("|")

    def is_winner(self, player):
        is_line_winner = is_winner_in_list(self.boardGame, player)
        is_column_winner = is_winner_in_list(
            [[line[column] for line in self.boardGame] for column in range(3)], player
        )
        is_left_to_right_diagonal_winner = is_winner_in_list(
            [[line[column] for column, line in enumerate(self.boardGame)]], player
        )
        is_right__to_left_diagonal_winner = is_winner_in_list(
            [[line[-column - 1] for column, line in enumerate(self.boardGame)]], player
        )
        return (
            is_line_winner
            or is_column_winner
            or is_left_to_right_diagonal_winner
            or is_right__to_left_diagonal_winner
        )

    def play(self, player):
        playable = False
        while not playable:
            x = int(input("give x coordinate between 0 and 2 \n>>>"))
            y = int(input("give y coordinate between 0 and 2 \n>>>"))
            playable = 0 <= x <= 2 and 0 <= y <= 2 and self.boardGame[x][y] != "-"
            if not playable:
                print("NOT PLAYABLE : you must give (x, y) between 0 and 2")
        self.boardGame[x][y] = player
