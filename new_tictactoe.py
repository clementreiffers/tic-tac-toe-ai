from tictactoe_constant import (
    WIDTH,
    HEIGHT,
    PLATEAU_TYPE,
    AV_POSITION_TYPE,
    COORD_TYPE,
)


def init_boardgame(void: str, width: int, height: int):
    return [[void for _ in range(width)] for _ in range(height)]


def stringify_boardgame(boardgame: list):
    return "".join("| " + " | ".join(i) + " |\n" for i in boardgame)


def show_boardgame(boardgame: PLATEAU_TYPE):
    print(stringify_boardgame(boardgame))


def play(player: str, coord: COORD_TYPE, boardgame: PLATEAU_TYPE) -> PLATEAU_TYPE:
    [x, y] = coord
    boardgame[y][x] = player
    return boardgame


def win(lst, player) -> bool:
    return any(line == [player] * 3 for line in lst)


def is_winner(player: str, plateau: PLATEAU_TYPE) -> bool:
    row_winner = win(plateau, player)
    col_winner = win([[row[col] for row in plateau] for col in range(3)], player)
    left_right_diag = win([[row[col] for col, row in enumerate(plateau)]], player)
    right_left_diag = win([[row[-col - 1] for col, row in enumerate(plateau)]], player)

    return row_winner or col_winner or left_right_diag or right_left_diag


def get_all_available_positions() -> AV_POSITION_TYPE:
    return [[x, y] for x in range(WIDTH) for y in range(HEIGHT)]
