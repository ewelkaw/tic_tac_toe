from pathlib import Path
from collections import namedtuple
from itertools import cycle 
import pygame
from game import Game
from pygame.locals import *

Player = namedtuple("Player", ["mark"])
IMAGES_PATH = Path(".").absolute().joinpath("images")
GAME_SIZE = (600,600)

IMAGES = {
    "e": pygame.image.load(str(IMAGES_PATH.joinpath("empty.png"))), 
    "o": pygame.image.load(str(IMAGES_PATH.joinpath("o_1.png"))),
    "x": pygame.image.load(str(IMAGES_PATH.joinpath("x_1.png"))),
    "start": pygame.image.load(str(IMAGES_PATH.joinpath("start_2.png"))),
    "game_over": pygame.image.load(str(IMAGES_PATH.joinpath("game_over.png")))
}

pygame.init()
WINDOW = pygame.display.set_mode(GAME_SIZE)
CLOCK = pygame.time.Clock()

def draw_board(game: Game):
    background = pygame.Surface(GAME_SIZE)
    WINDOW.blit(background, (0, 0))
    for i, element in enumerate(game.board):
        for j, _ in enumerate(element):
            img = IMAGES[game.board[i][j].status]
            WINDOW.blit(img, (i * 200, j * 200))
    pygame.display.flip()


def show_winner(winner: str):
    done = False
    while not done:
        pygame.display.set_caption(f" THE WINNER IS {winner.upper()}")
        draw(winner, (200, 200))

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (
                e.type == KEYUP
                and (e.key == K_RETURN or e.key == K_SPACE or e.key == K_ESCAPE)
            ):
                done = True

def game_over():
    done = False
    while not done:
        pygame.display.set_caption("GAME OVER")
        draw("game_over", (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == KEYUP and (e.key == K_RETURN or e.key == K_SPACE or e.key == K_ESCAPE)
            ):
                done = True
    

def start_game(starting_mark):
    game = Game()
    draw_board(game)

    user = Player(mark=starting_mark)
    computer = Player(mark="o") if starting_mark == "x" else Player(mark="x")

    players = [user, computer]
    for player in cycle(players):
        pygame.display.set_caption(f"Player {player.mark}")
        if game.finished:
            show_winner(game.winner)
            break
        elif not game.available_fields:
            game_over()
            break

        done = False
        while not done:
            for e in pygame.event.get():
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    x = e.pos[0] // 200
                    y = e.pos[1] // 200
                    if (x, y) in game.available_fields:
                        game.update_single_field(player.mark, (x,y))
                        draw_board(game)
                        done = True

def draw(img: str,size : tuple):
    img = IMAGES[img]
    WINDOW.fill([255,255,255])
    WINDOW.blit(img, size)
    pygame.display.flip()

def main():
    pygame.display.set_caption("Choose X or O")
    draw("start", (0, 0))

    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == KEYUP and (e.key == K_RETURN or e.key == K_SPACE or e.key == K_ESCAPE)):
                done = True
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if e.pos[0] in range(0, 300):
                    starting_mark = "x"
                    done = True
                if e.pos[0] in range(300,600):
                    starting_mark = "o"
                    done = True

    start_game(starting_mark)


if __name__ == "__main__":
    main()