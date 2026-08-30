import pytest

from game_search.tic_tac_toe import (
    Move,
    Player,
    State,
    TicTacToe,
    board_full,
    winner,
)


@pytest.fixture
def game():
    return TicTacToe()


def test_initial_state(game):
    state = game.initial_state()

    assert state.board == (None,) * 9
    assert state.player == Player.EX


def test_current_player(game):
    state = State((None,) * 9, Player.OH)

    assert game.current_player(state) == Player.OH


def test_legal_moves_empty_board(game):
    state = game.initial_state()

    assert game.legal_moves(state) == [
        Move(0),
        Move(1),
        Move(2),
        Move(3),
        Move(4),
        Move(5),
        Move(6),
        Move(7),
        Move(8),
    ]


def test_legal_moves_partially_filled(game):
    state = State(
        (
            Player.EX,
            None,
            Player.OH,
            None,
            Player.EX,
            None,
            Player.OH,
            None,
            None,
        ),
        Player.EX,
    )

    assert game.legal_moves(state) == [
        Move(1),
        Move(3),
        Move(5),
        Move(7),
        Move(8),
    ]


def test_make_move_places_player(game):
    state = game.initial_state()

    new_state = game.make_move(state, Move(4))

    assert new_state.board == (
        None,
        None,
        None,
        None,
        Player.EX,
        None,
        None,
        None,
        None,
    )


def test_make_move_switches_player(game):
    state = game.initial_state()

    new_state = game.make_move(state, Move(4))

    assert new_state.player == Player.OH


def test_make_move_does_not_modify_original_state(game):
    state = game.initial_state()

    game.make_move(state, Move(4))

    assert state.board == (None,) * 9
    assert state.player == Player.EX


@pytest.mark.parametrize(
    "board, expected_winner",
    [
        # Rows
        (
            (
                Player.EX,
                Player.EX,
                Player.EX,
                None,
                None,
                None,
                None,
                None,
                None,
            ),
            Player.EX,
        ),
        (
            (
                None,
                None,
                None,
                Player.OH,
                Player.OH,
                Player.OH,
                None,
                None,
                None,
            ),
            Player.OH,
        ),
        # Columns
        (
            (
                Player.EX,
                None,
                None,
                Player.EX,
                None,
                None,
                Player.EX,
                None,
                None,
            ),
            Player.EX,
        ),
        (
            (
                None,
                Player.OH,
                None,
                None,
                Player.OH,
                None,
                None,
                Player.OH,
                None,
            ),
            Player.OH,
        ),
        # Diagonals
        (
            (
                Player.EX,
                None,
                None,
                None,
                Player.EX,
                None,
                None,
                None,
                Player.EX,
            ),
            Player.EX,
        ),
        (
            (
                None,
                None,
                Player.OH,
                None,
                Player.OH,
                None,
                Player.OH,
                None,
                None,
            ),
            Player.OH,
        ),
    ],
)
def test_winner(board, expected_winner):
    state = State(board, Player.EX)

    assert winner(state) == expected_winner


def test_winner_no_winner():
    state = State(
        (
            Player.EX,
            Player.OH,
            None,
            None,
            Player.EX,
            None,
            None,
            None,
            Player.OH,
        ),
        Player.EX,
    )

    assert winner(state) is None


def test_winner_empty_board():
    state = State((None,) * 9, Player.EX)

    assert winner(state) is None


def test_board_full():
    state = State(
        (
            Player.EX,
            Player.OH,
            Player.EX,
            Player.OH,
            Player.EX,
            Player.OH,
            Player.OH,
            Player.EX,
            Player.OH,
        ),
        Player.EX,
    )

    assert board_full(state)


def test_board_not_full():
    state = State(
        (
            Player.EX,
            Player.OH,
            Player.EX,
            Player.OH,
            None,
            Player.OH,
            Player.OH,
            Player.EX,
            Player.OH,
        ),
        Player.EX,
    )

    assert not board_full(state)


def test_terminal_when_x_wins(game):
    state = State(
        (
            Player.EX,
            Player.EX,
            Player.EX,
            Player.OH,
            Player.OH,
            None,
            None,
            None,
            None,
        ),
        Player.OH,
    )

    assert game.is_terminal(state)


def test_terminal_when_board_full(game):
    state = State(
        (
            Player.EX,
            Player.OH,
            Player.EX,
            Player.OH,
            Player.EX,
            Player.OH,
            Player.OH,
            Player.EX,
            Player.OH,
        ),
        Player.EX,
    )

    assert game.is_terminal(state)


def test_not_terminal(game):
    state = State(
        (
            Player.EX,
            Player.OH,
            None,
            None,
            Player.EX,
            None,
            None,
            None,
            Player.OH,
        ),
        Player.EX,
    )

    assert not game.is_terminal(state)


def test_evaluate_x_win_for_x(game):
    state = State(
        (
            Player.EX,
            Player.EX,
            Player.EX,
            Player.OH,
            Player.OH,
            None,
            None,
            None,
            None,
        ),
        Player.OH,
    )

    assert game.evaluate(state, Player.EX) == 1


def test_evaluate_x_win_for_o(game):
    state = State(
        (
            Player.EX,
            Player.EX,
            Player.EX,
            Player.OH,
            Player.OH,
            None,
            None,
            None,
            None,
        ),
        Player.OH,
    )

    assert game.evaluate(state, Player.OH) == -1


def test_evaluate_draw(game):
    state = State(
        (
            Player.EX,
            Player.OH,
            Player.EX,
            Player.OH,
            Player.EX,
            Player.OH,
            Player.OH,
            Player.EX,
            Player.OH,
        ),
        Player.EX,
    )

    assert game.evaluate(state, Player.EX) == 0
