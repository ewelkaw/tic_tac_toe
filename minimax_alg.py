from math import inf as infinity
from collections import namedtuple

from const import Player
from game import Game


def evaluate(game: Game) -> bool:
    if game.finished and game.winner == "o":
        return 1
    elif game.finished and game.winner == "x":
        return -1
    else:
        return 0

def choose_best_move(game: Game, depth: int, player: Player) -> list:
    if player.player_name == "computer":
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or not game.available_fields:
        score = evaluate(game)
        return [-1, -1, score]

    for field in game.available_fields:
        new_game = game.copy()
        new_game.update_single_field(player.mark, field)

        if player.mark == "x" and player.player_name == "computer":
            score = choose_best_move(new_game, depth - 1, Player(mark='o', player_name="user"))
        elif player.mark == "x" and player.player_name == "user":
            score = choose_best_move(new_game, depth - 1, Player(mark='o', player_name="computer"))
        elif player.mark == "o" and player.player_name == "computer":
            score = choose_best_move(new_game, depth - 1, Player(mark='x', player_name="user"))
        elif player.mark == "o" and player.player_name == "user":
            score = choose_best_move(new_game, depth - 1, Player(mark='x', player_name="computer"))

        score[0], score[1] = field
        
        if player.player_name == "computer":
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best
