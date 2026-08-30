import os

from flask import Flask, redirect, render_template, request, session, url_for

from game_search.minimax import minimax
from game_search.tic_tac_toe import Player, State, TicTacToe, winner

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

game = TicTacToe()


def state_from_session() -> State:
    board = tuple(
        None if value is None else Player(value) for value in session["board"]
    )
    return State(board, Player(session["player"]))


def state_to_session(state: State) -> None:
    session["board"] = [None if value is None else value.value for value in state.board]
    session["player"] = state.player.value


@app.get("/")
def index():
    if "board" not in session:
        state_to_session(game.initial_state())

    state = state_from_session()
    game_winner = winner(state)

    return render_template(
        "index.html",
        board=state.board,
        player=state.player,
        terminal=game.is_terminal(state),
        winner=game_winner,
    )


@app.post("/move")
def move():
    state = state_from_session()

    position = int(request.form["position"])
    human_move = next(
        move for move in game.legal_moves(state) if move.position == position
    )

    state = game.make_move(state, human_move)

    if not game.is_terminal(state):
        computer_move, _ = minimax(game, state)
        state = game.make_move(state, computer_move)

    state_to_session(state)

    return redirect(url_for("index"))


@app.post("/new-game")
def new_game():
    state_to_session(game.initial_state())
    return redirect(url_for("index"))
