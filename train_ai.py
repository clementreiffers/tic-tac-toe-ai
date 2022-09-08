from random import shuffle

import numpy as np
import pandas as pd
from numpy import ndarray

from new_tictactoe import (
    init_boardgame,
    get_all_available_positions,
    show_boardgame,
    is_winner,
    play,
)
from tictactoe_constant import (
    PLATEAU_TYPE,
    VOID,
    WIDTH,
    HEIGHT,
    AV_POSITION_TYPE,
    J1,
    J2,
    COORD_TYPE,
)


def vectorize_boardgame(boardgame: PLATEAU_TYPE) -> str:
    return ",".join(map(lambda row: ",".join(row), boardgame))


def train_ai_j1():
    temp_his_pos: list[str] = []
    temp_his_coord: list[COORD_TYPE] = []

    while True:
        winner: bool = False
        j1_win: bool = False
        j2_win: bool = False
        current_positions: list[PLATEAU_TYPE] = []
        winner_coord: list[COORD_TYPE] = []

        bg: PLATEAU_TYPE = init_boardgame(VOID, WIDTH, HEIGHT)
        show_boardgame(bg)
        playable_pos: AV_POSITION_TYPE = get_all_available_positions()
        shuffle(playable_pos)
        while not winner and len(playable_pos) > 0:
            player: str = J1 if len(playable_pos) % 2 == 0 else J2
            print(f"--------- PLAYER '{player}' TO PLAY --------- ")

            coord: COORD_TYPE = playable_pos[-1]

            if vectorize_boardgame(bg) != "-,-,-,-,-,-,-,-,-":
                temp_his_coord.append(coord)
                temp_his_pos.append(vectorize_boardgame(bg))

            bg = play(player, coord, bg)

            j1_win = is_winner(J1, bg)
            j2_win = is_winner(J2, bg)
            playable_pos.remove(coord)
            show_boardgame(bg)
            winner = j2_win or j1_win

        if j1_win:
            print(f"******* {J1 if j1_win else J2 if j2_win else '??'} WIN !!*******")
            current_positions += temp_his_pos
            winner_coord += temp_his_coord

            winner_coord_numpy: ndarray = np.array(winner_coord)

            pd.DataFrame(
                {
                    "positions": current_positions,
                    "x": winner_coord_numpy[:, 0],
                    "y": winner_coord_numpy[:, 1],
                }
            ).to_csv("dataset.csv", index=False)


train_ai_j1()
