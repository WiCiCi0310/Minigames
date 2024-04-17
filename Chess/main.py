import pygame
import chessboard as cb
import chessman as cm

FPS = 60
WIDTH = HEIGHT = cb.TILE_SIZE*8

pygame.init()
pygame.display.set_caption("chess")
window = pygame.display.set_mode((WIDTH, HEIGHT))


def draw(window, chessboard: cb.Chessboard) -> None:
    chessboard.draw(window)
    for i in range(8):
        for j in range(8):
            if chessboard.board[i][j]:
                chessboard.board[i][j].draw(window)
    pygame.display.update()


def main(window) -> None:

    chessboard = cb.Chessboard()

    chessboard.board[0][0] = cm.Rook(
        0, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
    chessboard.board[0][1] = cm.Knight(
        1, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
    chessboard.board[0][2] = cm.Bishop(
        2, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
    chessboard.board[0][5] = cm.Bishop(
        5, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
    chessboard.board[0][6] = cm.Knight(
        6, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
    chessboard.board[0][7] = cm.Rook(
        7, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
    chessboard.board[0][3] = cm.Queen(
        3, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
    chessboard.board[0][4] = cm.King(
        4, 0, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")

    chessboard.board[7][0] = cm.Rook(
        0, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")
    chessboard.board[7][1] = cm.Knight(
        1, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")
    chessboard.board[7][2] = cm.Bishop(
        2, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")
    chessboard.board[7][5] = cm.Bishop(
        5, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")
    chessboard.board[7][6] = cm.Knight(
        6, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")
    chessboard.board[7][7] = cm.Rook(
        7, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")
    chessboard.board[7][3] = cm.Queen(
        3, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")
    chessboard.board[7][4] = cm.King(
        4, 7, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")

    for i in range(8):
        chessboard.board[1][i] = cm.Pawn(
            i, 1, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "White")
        chessboard.board[6][i] = cm.Pawn(
            i, 6, cm.CHESSMAN_WIDTH, cm.CHESSMAN_HEIGHT, "Black")

    running = True
    colors = ["Black", "White"]
    turn = True
    selecting_sth = False
    curr_x = curr_y = -1

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not selecting_sth:
                curr_x, curr_y = pygame.mouse.get_pos()
                curr_x //= cb.TILE_SIZE
                curr_y //= cb.TILE_SIZE

                if chessboard.board[curr_y][curr_x] and \
                        chessboard.board[curr_y][curr_x].color == colors[int(turn)]:
                    selecting_sth = True
                    chessboard.board[curr_y][curr_x].is_selected(chessboard)

            elif event.type == pygame.MOUSEBUTTONDOWN and selecting_sth:

                x, y = pygame.mouse.get_pos()
                x //= cb.TILE_SIZE
                y //= cb.TILE_SIZE
                turn = not turn if chessboard.board[curr_y][curr_x].move(
                    chessboard, (curr_x, curr_y), (x, y)) else turn

                curr_x, curr_y = -1, -1
                selecting_sth = False

        draw(window, chessboard)

    pygame.quit()
    exit()


if __name__ == "__main__":
    main(window)
