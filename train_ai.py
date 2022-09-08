import pickle
from random import shuffle

import numpy as np
from numpy import ndarray
from pandas import DataFrame, read_csv
from sklearn.ensemble import RandomForestClassifier

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
    MODEL_FILENAME,
)


def vectorize_boardgame(boardgame: PLATEAU_TYPE) -> str:
    return ",".join(map(lambda row: ",".join(row), boardgame))


def generate_j1_dataset(epochs: int, verbose: bool):
    temp_his_pos: list[str] = []
    temp_his_coord: list[COORD_TYPE] = []

    while epochs > len(temp_his_pos):
        print(len(temp_his_pos)) if len(temp_his_pos) % 1000 == 0 else ...
        winner: bool = False
        j1_win: bool = False
        j2_win: bool = False
        current_positions: list[PLATEAU_TYPE] = []
        winner_coord: list[COORD_TYPE] = []

        bg: PLATEAU_TYPE = init_boardgame(VOID, WIDTH, HEIGHT)
        show_boardgame(bg) if verbose else ...
        playable_pos: AV_POSITION_TYPE = get_all_available_positions()
        shuffle(playable_pos)
        while not winner and len(playable_pos) > 0:
            player: str = J1 if len(playable_pos) % 2 == 0 else J2
            print(f"--------- PLAYER '{player}' TO PLAY --------- ") if verbose else ...

            coord: COORD_TYPE = playable_pos[-1]

            temp_his_coord.append(coord)
            temp_his_pos.append(vectorize_boardgame(bg))

            bg = play(player, coord, bg)

            j1_win = is_winner(J1, bg)
            j2_win = is_winner(J2, bg)
            playable_pos.remove(coord)
            show_boardgame(bg) if verbose else ...
            winner = j2_win or j1_win

        if j2_win:
            print(
                f"******* {J1 if j1_win else J2 if j2_win else '??'} WIN !!*******"
            ) if verbose else ...
            current_positions += temp_his_pos
            winner_coord += temp_his_coord

            winner_coord_numpy: ndarray = np.array(winner_coord)

            DataFrame(
                {
                    "positions": current_positions,
                    "x": winner_coord_numpy[:, 0],
                    "y": winner_coord_numpy[:, 1],
                }
            ).to_csv("dataset.csv", index=False)


def convert_character_to_number(char):
    return 0 if char == "-" else 1 if char == "X" else 2


def convert_vectorstr_to_vectorint(vectorstr: str):
    return list(map(convert_character_to_number, vectorstr.split(",")))


def save_ai(model):
    with open(MODEL_FILENAME, "wb") as files:
        pickle.dump(model, files)


def read_model():
    with open(MODEL_FILENAME, "rb") as f:
        return pickle.load(f)


def train_ai(dataset: str):
    df = read_csv(dataset)
    x = list(map(convert_vectorstr_to_vectorint, df.positions.tolist()))
    y = df.drop("positions", axis=1)
    rf = RandomForestClassifier()
    rf.fit(x, y)
    save_ai(rf)
    return rf


generate_j1_dataset(10000, False)
train_ai("dataset.csv")
