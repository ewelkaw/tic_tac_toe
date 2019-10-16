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
    "o": pygame.image.load(str(IMAGES_PATH.joinpath("o.png"))),
    "x": pygame.image.load(str(IMAGES_PATH.joinpath("x.png"))),
    "start": pygame.image.load(str(IMAGES_PATH.joinpath("start.png"))),
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
        pygame.display.set_caption(" THE WINNER IS {}".format(winner))
        img = IMAGES[winner]
        WINDOW.fill([255,255,255])
        WINDOW.blit(img, (200, 200))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (
                e.type == KEYUP
                and (e.key == K_RETURN or e.key == K_SPACE or e.key == K_ESCAPE)
            ):
                done = True
                break

def game_over():
    done = False
    while not done:
        pygame.display.set_caption("GAME OVER")
        img = IMAGES["game_over"]
        WINDOW.fill([255,255,255])
        WINDOW.blit(img, (0, 0))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (
                e.type == KEYUP
                and (e.key == K_RETURN or e.key == K_SPACE or e.key == K_ESCAPE)
            ):
                done = True
                break
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                main()

def start_game(starting_mark):
    game = Game()
    draw_board(game)

    user = Player(mark=starting_mark)
    computer = Player(mark="o") if starting_mark == "x" else Player(mark="x")

    players = [user, computer]
    for player in cycle(players):
        if game.finished:
            show_winner(game.winner)
        if not game.avaliable_fields:
            game_over()
        done = False
        while not done:
            for e in pygame.event.get():
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    x = e.pos[0] // 200
                    y = e.pos[1] // 200
                    if (x, y) in game.avaliable_fields:
                        game.update_single_field(player.mark, (x,y))
                        draw_board(game)
                        done = True

def main():
    pygame.display.set_caption("Choose X or O")
    img = IMAGES["start"]
    WINDOW.fill([180,180,180])
    WINDOW.blit(img, (0, 0))
    pygame.display.flip()

    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if e.pos[0] in range(0, 300) and e.pos[1] in range(0, 300):
                    starting_mark = "x"
                    done = True
                if e.pos[0] in range(300,600) and e.pos[1] in range(300,600):
                    starting_mark = "o"
                    done = True

    start_game(starting_mark)


if __name__ == "__main__":
    main()