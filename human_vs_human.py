from new_tictactoe import (
    init_boardgame,
    get_all_available_positions,
    show_boardgame,
    play,
    is_winner,
)
from tictactoe_constant import (
    WIDTH,
    HEIGHT,
    COORD_TYPE,
    AV_POSITION_TYPE,
    PLATEAU_TYPE,
    VOID,
    J1,
    J2,
)


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

    print(f"******* {J1 if j1_win else J2 if j2_win else '??'} WIN !!*******")
