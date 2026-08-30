from dataclasses import dataclass
from enum import Enum

# 0 | 1 | 2
# ---------
# 3 | 4 | 5
# ---------
# 6 | 7 | 8

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class Player(Enum):
    EX = "X"
    OH = "O"


@dataclass(frozen=True)
class State:
    board: tuple[Player | None, ...]
    player: Player


@dataclass(frozen=True)
class Move:
    position: int


def winner(state: State) -> Player | None:
    for line in WINNING_LINES:
        first = state.board[line[0]]

        if first is not None and first == state.board[line[1]] == state.board[line[2]]:
            return first

    return None


def board_full(state: State) -> bool:
    return not any(value is None for value in state.board)


class TicTacToe:
    def initial_state(self) -> State:
        initial_board = (None,) * 9
        initial_player = Player.EX
        return State(initial_board, initial_player)

    def current_player(self, state: State) -> Player:
        return state.player

    def legal_moves(self, state: State) -> list[Move]:
        valid_moves = []
        for index, val in enumerate(state.board):
            if val is None:
                valid_moves.append(Move(index))

        return valid_moves

    def make_move(self, state: State, move: Move) -> State:
        tokens = list(state.board)
        tokens[move.position] = state.player
        new_player = Player.OH if state.player == Player.EX else Player.EX
        return State(tuple(tokens), new_player)

    def is_terminal(self, state: State) -> bool:
        return winner(state) is not None or board_full(state)

    def evaluate(self, state: State, player: Player) -> float:
        winning_player = winner(state)
        if winning_player is None:
            return 0
        elif winning_player == player:
            return 1
        else:
            return -1

    def display(self, state: State) -> None:
        board = state.board

        for row in range(3):
            start = row * 3
            print(
                " | ".join(
                    " " if board[i] is None else board[i].value
                    for i in range(start, start + 3)
                )
            )

            if row < 2:
                print("---------")
