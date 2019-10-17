import random

import pytest

from game import Game


def prepare_fields(
    game: Game, o_fields_positions: list, x_fields_positions: list
) -> Game:
    if o_fields_positions:
        for i in o_fields_positions:
            game.update_single_field("o", i)
    if x_fields_positions:
        for i in x_fields_positions:
            game.update_single_field("x", i)
    return game


@pytest.mark.parametrize("input,expected", [(0, 3), (1, 3), (2, 3)])
def test_create_game(input, expected):
    game = Game()
    assert len(game.board) == 3
    assert len(game.board[input]) == expected
    assert game.board[random.choice([0, 1, 2])][random.choice([0, 1, 2])].status == "e"
    assert game.board[random.choice([0, 1, 2])][
        random.choice([0, 1, 2])
    ].status not in ["x", "o"]


def test_update_game_field():
    game = Game()
    game.update_single_field("x", (1, 2))
    game.update_single_field("o", (1, 2))
    game.update_single_field("o", (2, 2))
    assert game.board[1][2].status == "x"
    assert game.board[1][2].status != "o"
    assert game.board[2][2].status == "o"


def test_finish_game_success_o():
    game = Game()
    o_fields_positions = [(0, 0), (0, 1), (0, 2)]
    game = prepare_fields(game, o_fields_positions, None)
    assert game.finished == True


def test_finish_game_success_x():
    game = Game()
    x_fields_positions = [(0, 0), (0, 1), (0, 2), (2, 1)]
    game = prepare_fields(game, None, x_fields_positions)
    assert game.finished == True


def test_finish_game_success():
    game = Game()
    o_fields_positions = [(2, 0), (2, 1), (2, 2)]
    x_fields_positions = [(0, 0), (1, 1)]
    game = prepare_fields(game, o_fields_positions, x_fields_positions)
    assert game.finished == True


def test_finish_game_failure():
    game = Game()
    o_fields_positions = [(0, 0), (0, 1), (1, 1)]
    x_fields_positions = [(1, 2), (2, 1)]
    game = prepare_fields(game, o_fields_positions, x_fields_positions)
    assert game.finished == False


def test_avaliable_fields():
    game = Game()
    o_fields_positions = [(0, 0), (0, 1), (1, 1)]
    x_fields_positions = [(1, 2), (2, 1)]
    game = prepare_fields(game, o_fields_positions, x_fields_positions)

    assert len(game.available_fields) == 4
    assert set(game.available_fields) == set([(2, 0), (2, 2), (0, 2), (1, 0)])


def test_one_avaliable_fields():
    game = Game()
    o_fields_positions = [(0, 0), (0, 1), (1, 1), (2, 0), (2, 2)]
    x_fields_positions = [(0, 2), (1, 2), (2, 1)]
    game = prepare_fields(game, o_fields_positions, x_fields_positions)
    assert game.available_fields == [(1, 0)]


def test_no_avaliable_fields():
    game = Game()
    o_fields_positions = [(0, 0), (0, 1), (1, 1), (2, 0), (2, 2)]
    x_fields_positions = [(0, 2), (1, 0), (1, 2), (2, 1)]
    game = prepare_fields(game, o_fields_positions, x_fields_positions)
    assert game.available_fields == []
