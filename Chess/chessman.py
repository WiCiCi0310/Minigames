import pygame
import chessboard as cb
from os.path import join


CHESSMAN_WIDTH = 32
CHESSMAN_HEIGHT = 128

pygame.display.set_mode((100, 100))


def load_chessmans(width: int, height: int) -> dict[str: dict]:

    image = pygame.image.load(join("assets", "chessman.png")).convert_alpha()
    chessmans = {"Black": {}, "White": {}}
    names = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]

    for i in range(image.get_width() // width):

        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(i * width, 0, width, height)
        surface.blit(image, (0, 0), rect)
        chessmans["White"][names[i]] = surface

        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(i * width, height, width, height)
        surface.blit(image, (0, 0), rect)
        chessmans["Black"][names[i]] = surface

    return chessmans


class Chessman:

    CHESSMANS = load_chessmans(CHESSMAN_WIDTH, CHESSMAN_HEIGHT)

    def __init__(self, x: int, y: int, width: int, height: int, color: str, name: str) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.name = name
        self.image = self.CHESSMANS[color][name]
        self.move_count = 0
        self.selected = False
        self.addition_moves = []
        self.all_moves = []

    def draw(self, window: pygame.Surface):
        if self.selected:
            for move in self.all_moves:
                pygame.draw.circle(window, (0, 50, 160),
                                   (move[0]*cb.TILE_SIZE + cb.TILE_SIZE//2, move[1]*cb.TILE_SIZE + cb.TILE_SIZE//2), 20)

        window.blit(self.image, (self.rect.x *
                                 cb.TILE_SIZE + CHESSMAN_WIDTH // 2,
                                 self.rect.y * cb.TILE_SIZE - CHESSMAN_HEIGHT // 2 - int(self.selected)*20))

    def get_possible_move(self) -> list[tuple]:
        pass

    def is_in_board(self, x: int, y: int = 0) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

    def move(self, chessboard: cb.Chessboard, curr_pos: tuple[int, int], dest_pos: tuple[int, int]) -> bool:
        moved = False
        if self.selected and (dest_pos in self.all_moves):
            if curr_pos != dest_pos:
                curr_x, curr_y = curr_pos
                dest_x, dest_y = dest_pos

                enemy = "Black" if self.color == "White" else "White"
                if chessboard.board[dest_y][dest_x]:
                    chessboard.defeated_chessmans[enemy].append(
                        chessboard.board[dest_y][dest_x])
                chessboard.board[dest_y][dest_x] = chessboard.board[curr_y][curr_x]
                chessboard.board[curr_y][curr_x] = None

                moved = True
                self.addition_moves = []

                self.rect.x, self.rect.y = dest_pos
                self.move_count += 1

                chessboard.has_a_winner(self.color, King)

        self.selected = False
        self.all_moves = []
        return moved

    def is_selected(self, chessboard: cb.Chessboard) -> None:
        self.selected = True
        self.all_moves = [
            *self.get_possible_move(chessboard.board), *self.addition_moves]


class Pawn(Chessman):
    def __init__(self, x: int, y: int, width: int, height: int, color: str) -> None:
        super().__init__(x, y, width, height, color, "Pawn")

    def move(self, chessboard: cb.Chessboard, curr_pos: tuple, dest_pos: tuple) -> bool:
        ret = super().move(chessboard, curr_pos, dest_pos)
        self.promote(chessboard.board)
        return ret

    def get_possible_move(self, board: list[list[Chessman]]) -> list[tuple]:

        bound = 3 if self.move_count == 0 else 2
        indicator = 1 if self.color == "White" else -1
        # indicator use to flip the result for different colors
        moves = [(self.rect.x, self.rect.y)]

        for i in range(1, bound):
            if self.is_in_board(self.rect.x, self.rect.y + i*indicator)\
                    and not board[self.rect.y + i*indicator][self.rect.x]:
                moves.append((self.rect.x, self.rect.y + i*indicator))
            else:
                break

        if self.is_in_board(self.rect.x - indicator, self.rect.y + indicator) \
                and board[self.rect.y + indicator][self.rect.x - indicator]:
            if board[self.rect.y + indicator][self.rect.x - indicator].color != self.color:
                moves.append((self.rect.x - indicator,
                              self.rect.y + indicator))

        if self.is_in_board(self.rect.x + indicator, self.rect.y + indicator) \
                and board[self.rect.y + indicator][self.rect.x + indicator]:
            if board[self.rect.y + indicator][self.rect.x + indicator].color != self.color:
                moves.append((self.rect.x + indicator,
                             self.rect.y + indicator))

        return moves

    def promote(self, board: list[list[Chessman]]) -> None:
        if (self.color == "White" and self.rect.y == 7) or (self.color == "Black" and self.rect.y == 0):
            board[self.rect.y][self.rect.x] = Queen(
                self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.color)


class Rook(Chessman):

    def __init__(self, x: int, y: int, width: int, height: int, color: str):
        super().__init__(x, y, width, height, color, "Rook")

    def add_moves(self, dx: int, dy: int, board: list[list[Chessman]], moves: list[tuple[int, int]]) -> None:
        while self.is_in_board(self.rect.x + dx, self.rect.y + dy):
            if not board[self.rect.y + dy][self.rect.x + dx]:
                moves.append((self.rect.x + dx, self.rect.y + dy))
                dx = 0 if dx == 0 else dx + dx // abs(dx)
                dy = 0 if dy == 0 else dy + dy // abs(dy)
            else:
                if board[self.rect.y + dy][self.rect.x + dx].color != self.color:
                    moves.append((self.rect.x + dx, self.rect.y + dy))
                break

    def get_possible_move(self, board: list[list[Chessman]]) -> list[tuple]:
        moves = [(self.rect.x, self.rect.y)]

        Rook.add_moves(self, 1, 0, board, moves)
        Rook.add_moves(self, -1, 0, board, moves)
        Rook.add_moves(self, 0, 1, board, moves)
        Rook.add_moves(self, 0, -1, board, moves)

        return moves


class Knight(Chessman):
    def __init__(self, x: int, y: int, width: int, height: int, color: str) -> None:
        super().__init__(x, y, width, height, color, "Knight")

    def get_possible_move(self, board: list[list[Chessman]]) -> list[tuple]:
        moves = [(self.rect.x, self.rect.y)]

        def add_moves(dx: int, dy: int) -> None:
            if self.is_in_board(self.rect.x + dx, self.rect.y + dy):
                if not board[self.rect.y + dy][self.rect.x + dx] or board[self.rect.y + dy][self.rect.x + dx].color != self.color:
                    moves.append((self.rect.x + dx, self.rect.y + dy))

        add_moves(2, 1)
        add_moves(2, -1)
        add_moves(-2, 1)
        add_moves(-2, -1)
        add_moves(1, 2)
        add_moves(1, -2)
        add_moves(-1, 2)
        add_moves(-1, -2)

        return moves


class Bishop(Chessman):
    def __init__(self, x: int, y: int, width: int, height: int, color: str) -> None:
        super().__init__(x, y, width, height, color, "Bishop")

    def add_moves(self, dx: int, dy: int, board: list[list[Chessman]], moves: list[tuple[int, int]]) -> None:
        while self.is_in_board(self.rect.x + dx, self.rect.y + dy):
            if not board[self.rect.y + dy][self.rect.x + dx] or board[self.rect.y + dy][self.rect.x + dx].color != self.color:
                moves.append((self.rect.x + dx, self.rect.y + dy))
                dx += dx // abs(dx)
                dy += dy // abs(dy)
            else:
                break

    def get_possible_move(self, board: list[list[Chessman]]) -> list[tuple]:
        moves = [(self.rect.x, self.rect.y)]

        Bishop.add_moves(self, 1, 1, board, moves)
        Bishop.add_moves(self, 1, -1, board, moves)
        Bishop.add_moves(self, -1, 1, board, moves)
        Bishop.add_moves(self, -1, -1, board, moves)

        return moves


class Queen(Chessman):
    def __init__(self, x: int, y: int, width: int, height: int, color: str) -> None:
        super().__init__(x, y, width, height, color, "Queen")

    def get_possible_move(self, board: list[list[Chessman]]) -> list[tuple]:
        moves = [(self.rect.x, self.rect.y)]

        Rook.add_moves(self, 1, 0, board, moves)
        Rook.add_moves(self, -1, 0, board, moves)
        Rook.add_moves(self, 0, 1, board, moves)
        Rook.add_moves(self, 0, -1, board, moves)

        Bishop.add_moves(self, 1, 1, board, moves)
        Bishop.add_moves(self, 1, -1, board, moves)
        Bishop.add_moves(self, -1, 1, board, moves)
        Bishop.add_moves(self, -1, -1, board, moves)

        return moves


class King(Chessman):
    def __init__(self, x: int, y: int, width: int, height: int, color: str) -> None:
        super().__init__(x, y, width, height, color, "King")

    def castle(self, board: list[list[Chessman]], dest_pos: tuple[int, int]):
        if dest_pos == (0, self.rect.y) and board[self.rect.y][1] == board[self.rect.y][2] == board[self.rect.y][3] == None:
            if self.move_count == 0 and board[self.rect.y][0]:
                if (board[self.rect.y][0].name == "Rook"
                    and board[self.rect.y][0].color == self.color
                        and board[self.rect.y][0].move_count == 0):

                    board[self.rect.y][2] = board[self.rect.y][0]
                    board[self.rect.y][2].rect.x = 2

                    self.addition_moves.append((1, self.rect.y))
                    dest_pos = (1, self.rect.y)

                    board[self.rect.y][2].move_count = 1
                    board[self.rect.y][0] = None

        elif dest_pos == (7, self.rect.y) and board[self.rect.y][5] == board[self.rect.y][6] == None:
            if self.move_count == 0 and board[self.rect.y][7]:
                if (board[self.rect.y][7].name == "Rook"
                    and board[self.rect.y][7].color == self.color
                        and board[self.rect.y][7].move_count == 0):

                    board[self.rect.y][5] = board[self.rect.y][7]
                    board[self.rect.y][5].rect.x = 5
                    board[self.rect.y][5].move_count = 1
                    board[self.rect.y][7] = None

                    self.addition_moves.append((6, self.rect.y))
                    dest_pos = (6, self.rect.y)

        return dest_pos

    def move(self, chessboard: cb.Chessboard, curr_pos: tuple[int, int], dest_pos: tuple[int, int]) -> bool:
        dest_pos = self.castle(chessboard.board, dest_pos)
        if len(self.addition_moves) > 0:
            self.all_moves.append(*self.addition_moves)
        return super().move(chessboard, curr_pos, dest_pos)

    def get_possible_move(self, board: list[list[Chessman]]) -> list[tuple]:
        moves = [(self.rect.x, self.rect.y)]

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directions:
            dx, dy = direction
            if self.is_in_board(self.rect.x + dx, self.rect.y + dy):
                if not board[self.rect.y + dy][self.rect.x + dx] or board[self.rect.y + dy][self.rect.x + dx].color != self.color:
                    moves.append((self.rect.x + dx, self.rect.y + dy))

        if board[self.rect.y][1] == board[self.rect.y][2] == board[self.rect.y][3] == None:
            if self.move_count == 0 and board[self.rect.y][7]:
                if (board[self.rect.y][7].name == "Rook"
                    and board[self.rect.y][7].color == self.color
                        and board[self.rect.y][7].move_count == 0):
                    moves.append((7, self.rect.y))

        if board[self.rect.y][5] == board[self.rect.y][6] == None:
            if self.move_count == 0 and board[self.rect.y][0]:
                if (board[self.rect.y][0].name == "Rook"
                    and board[self.rect.y][0].color == self.color
                        and board[self.rect.y][0].move_count == 0):
                    moves.append((0, self.rect.y))

        return moves
