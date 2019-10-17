from collections import namedtuple

BOARD_SIZE = [3,3]
Field = namedtuple("Field", ["status", "status_img"])

FIELDS = {
    "x": ("x", "x.png"),
    "o": ("o", "o.png"),
    "e": ("e", "empty.png")
}

WINNING_COMBINATIONS = [
    ((0,0),(0,1),(0,2)),
    ((1,0),(1,1),(1,2)),
    ((2,0),(2,1),(2,2)),
    ((0,0),(1,0),(2,0)),
    ((0,1),(1,1),(2,1)),
    ((0,2),(1,2),(2,2)),
    ((0,0),(1,1),(2,2)),
    ((2,0),(1,1),(0,2))
]

class Game:
    def __init__(self):
        self.board = self.__setup_board()
        self.winner = None

    def __setup_board(self):
        board = []
        for i in range(BOARD_SIZE[0]):
            board.append([])
            for j in range(BOARD_SIZE[1]):
                board[i].append(Field(status=FIELDS["e"][0], status_img=FIELDS["e"][1]))
        return board

    def update_single_field(self, value: str, position: tuple) -> list:
        x, y = position
        if self.board[x][y].status == FIELDS["e"][0]:
            self.board[x][y] = Field(status=FIELDS[value][0], status_img=FIELDS[value][1])
        return self.board

    @property
    def finished(self) -> bool:
        for combination in WINNING_COMBINATIONS:
            x, y, z = combination
            x_object = self.board[x[0]][x[1]]
            y_object = self.board[y[0]][y[1]]
            z_object = self.board[z[0]][z[1]]
 
            if len(list(filter(lambda x: x.status != "e", [x_object, y_object, z_object]))) == 3:
                if x_object.status == y_object.status == z_object.status:
                    self.winner = x_object.status
                    return True
        return False

    @property
    def available_fields(self) -> list:
        available_fields = []
        for i in range(BOARD_SIZE[0]):
            for j in range(BOARD_SIZE[1]):
                if self.board[i][j].status == "e":
                    available_fields.append((i,j))
        return available_fields