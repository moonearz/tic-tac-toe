import math

from .game import Game, Move, Player, State


def minimax(
    game: Game, state: State, maximizing_player: Player | None = None
) -> tuple[Move, float]:
    if maximizing_player is None:
        maximizing_player = game.current_player(state)
    if game.is_terminal(state):
        return None, game.evaluate(state, maximizing_player)

    legal_moves = game.legal_moves(state)
    is_maximizing = game.current_player(state) == maximizing_player
    best_move = legal_moves[0]
    best_value = -math.inf if is_maximizing else math.inf

    for move in legal_moves:
        outcome_state = game.make_move(state, move)
        _, value = minimax(game, outcome_state, maximizing_player)

        if is_maximizing:
            if value > best_value:
                best_value = value
                best_move = move
        else:
            if value < best_value:
                best_value = value
                best_move = move

    return best_move, best_value
