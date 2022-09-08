import numpy as np

from human_vs_human import ask_verify_coordinates
from new_tictactoe import (
    init_boardgame,
    get_all_available_positions,
    show_boardgame,
    play,
    is_winner,
)
from tictactoe_constant import (
    PLATEAU_TYPE,
    VOID,
    WIDTH,
    HEIGHT,
    AV_POSITION_TYPE,
    COORD_TYPE,
    J1,
    J2,
)
from train_ai import read_model, convert_vectorstr_to_vectorint, vectorize_boardgame


def preprocess_input(bg: PLATEAU_TYPE):
    return list(
        np.array(convert_vectorstr_to_vectorint(vectorize_boardgame(bg))).reshape(1, -1)
    )


def human_vs_ai():
    bg: PLATEAU_TYPE = init_boardgame(VOID, WIDTH, HEIGHT)
    playable_pos: AV_POSITION_TYPE = get_all_available_positions()

    winner: bool = False
    j1_win: bool = False
    j2_win: bool = False
    model = read_model()
    show_boardgame(bg)

    while not winner:
        player: str = J1 if len(playable_pos) % 2 == 0 else J2
        show_boardgame(bg)
        if player == J1:
            print(f"--------- PLAYER '{player}' TO PLAY --------- ")
            coord: COORD_TYPE = ask_verify_coordinates(playable_pos)
            bg = play(player, coord, bg)
            j1_win = is_winner(J1, bg)
            winner = j2_win or j1_win
        else:
            coord = list(model.predict(preprocess_input(bg))[0])
            bg = play(player, coord, bg)
            j2_win = is_winner(J2, bg)
            print(f"AI CHOOSE {coord}")
        playable_pos.remove(coord)

    print(f"******* {J1 if j1_win else J2 if j2_win else '??'} WIN !!*******")


human_vs_ai()
