import pygame
from os.path import join

TILE_SIZE = 64

def get_tile(size: int, name: str):
    path = join("assets", "Tiles", name + ".png")
    image = pygame.image.load(path)
    return image

class Chessboard:

    def __init__(self):

        self.board = [[None] * 8 for i in range(8)]
        self.defeated_chessmans = {"Black": [], "White": []}
        self.tile_types = (get_tile(TILE_SIZE, "Black"),
                           get_tile(TILE_SIZE, "White"))
        self.chessboard_tiles = []

        for j in range(8):
            for i in range(8):
                self.chessboard_tiles.append(
                    [self.tile_types[(i + j) % 2], (i * TILE_SIZE, j*TILE_SIZE)])

    def draw(self, window):
        for tile in self.chessboard_tiles:
            window.blit(*tile)

    def has_a_winner(self, current_color_turn: str, check):
        opposite_color = "White" if current_color_turn == "Black" else "Black"
        for chessman in self.defeated_chessmans[opposite_color]:
            if type(chessman) == check:

                print(current_color_turn + " win!")
