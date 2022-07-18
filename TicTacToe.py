def is_winner_in_list(list, player):
    return any(line == [player] * 3 for line in list)


class TicTacToe:
    def __init__(self):
        self.board_game = []
        self.init_board_game()

        self.J1 = "X"
        self.J2 = "O"

    def init_board_game(self):
        self.board_game = [["-" for _ in range(3)] for _ in range(3)]

    def launch_game(self):
        while not (self.is_winner(self.J1) or self.is_winner(self.J2)):
            self.show_game()
            self.play_human(self.J1)
            if self.is_winner(self.J1):
                print("J1 win !")
                break
            self.show_game()
            self.play_human(self.J2)
            if self.is_winner(self.J2):
                print("J2 win !")
                break

    def show_game(self):
        print("-" * 13)
        for line in self.board_game:
            for value in line:
                print(f"| {value} ", end="")
            print("|")

    def is_winner(self, player):
        is_line_winner = is_winner_in_list(self.board_game, player)
        is_column_winner = is_winner_in_list(
            [[line[column] for line in self.board_game] for column in range(3)], player
        )
        is_left_to_right_diagonal_winner = is_winner_in_list(
            [[line[column] for column, line in enumerate(self.board_game)]], player
        )
        is_right__to_left_diagonal_winner = is_winner_in_list(
            [[line[-column - 1] for column, line in enumerate(self.board_game)]], player
        )
        return (
            is_line_winner
            or is_column_winner
            or is_left_to_right_diagonal_winner
            or is_right__to_left_diagonal_winner
        )

    def play_human(self, player):
        playable = False
        while not playable:
            x = int(input("give x coordinate between 0 and 2 \n>>>"))
            y = int(input("give y coordinate between 0 and 2 \n>>>"))
            playable = self.play(x, y, player)

    def play(self, x, y, player):
        playable = 0 <= x <= 2 and 0 <= y <= 2 and self.board_game[x][y] == "-"
        if not playable:
            print(
                f"NOT PLAYABLE : you must give (x, y) between 0 and 2 you played ({x}, {y})"
            )
        else:
            self.board_game[x][y] = player
        self.show_game()
        return playable
