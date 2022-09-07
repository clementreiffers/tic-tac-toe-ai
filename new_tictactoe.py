from tictactoe_constant import (
    WIDTH,
    HEIGHT,
    VOID,
    J1,
    J2,
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


def ask_coord_ax(ax: str) -> int:
    coord_given: str = input(f"give {ax} coordinate\n>>>")
    max_coord: int = WIDTH if ax == "x" else HEIGHT
    while not (coord_given.isdigit() and 0 <= int(coord_given) < max_coord):
        print("please enter a valid coordinate")
        coord_given = input(f"give {ax} coordinate\n>>>")
    return int(coord_given)


def ask_coordinates() -> COORD_TYPE:
    return [ask_coord_ax("x"), ask_coord_ax("y")]


def ask_verify_coordinates(playable_pos: AV_POSITION_TYPE) -> COORD_TYPE:
    coord: COORD_TYPE = ask_coordinates()
    while coord not in playable_pos:
        print("please give coordinates not played yet")
        coord = ask_coordinates()
    return coord


def human_vs_human():
    bg: PLATEAU_TYPE = init_boardgame(VOID, WIDTH, HEIGHT)
    playable_pos: AV_POSITION_TYPE = get_all_available_positions()

    winner: bool = False
    j1_win: bool = False
    j2_win: bool = False
    show_boardgame(bg)

    while not winner:
        player: str = J1 if len(playable_pos) % 2 == 0 else J2
        print(f"--------- PLAYER '{player}' TO PLAY --------- ")
        coord: COORD_TYPE = ask_verify_coordinates(playable_pos)
        bg = play(player, coord, bg)
        playable_pos.remove(coord)
        j1_win = is_winner(J1, bg)
        j2_win = is_winner(J2, bg)
        show_boardgame(bg)
        winner = j2_win or j1_win

    print(f"******* {J1 if j1_win else J2} WIN !!*******")


human_vs_human()
